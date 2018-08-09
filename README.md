# k4

**__THIS IS A WORK IN PROGRESS. IT IS STILL BEING PLANNED. NO COMPILER EXISTS
YET__**

Experimental/Toy strongly-typed language targeting microcontrollers.

# General Thoughts

My main target is the AVR, but there shouldn't be anything that prevents
it from being used elsewhere.

There will be no concept of a "reference" in the C-way. There will be an
`address` type, but it is effectively defined at compiler time and constant,
cannot be mutated, and the address cannot be used in an expression as any
reference to the variable will immediately dereference. The concept of "taking
the address of a variable" is non-existent.

Everything is statically dispatched. Objects are not tagged in memory with
their type.

Tail Call Optimizations should be done when possible. (I'm still mulling over
what a good register assignment/storage method would be and how to do this
effectively or what needs to be present syntactically to help if it's difficult
to do automatically.)

`match`es will be exhaustive.

`<=` denotes something being moved/loaded from memory.

`:=` denotes a definition

`{}` denotes a type parameter and is something known at compile time and will
require a new version of the function

`<>` denotes a type parameter and is something known at compile time and will
not require a new version of the function (but could).

For instance, `{}` is used to determine the type of a parameters and variables
and `<>` could be the length of an array or the number of iterations a function
requires. Length of an array will need to be `{}` for allocation, but for a
function that is looping over the array, `<>` will work.

(I'm not entirly sold on the above concept yet.)

## References

Variables that are the type of a record live a dual existance. They are
treated as references by most of the code, e.g. they are not copied
byte-by-byte when being passed to a function, but assignment and
swapping will work at the byte. For instance,

    record Point:
      int8 x
      int8 y

    a <- Point { x <- 1, y <- 2 }
    b <- Point { x <- 3, y <- 4 }

    # Does not create copies of a or b
    # Modifying a or b in `add` will cause a or b to be changed
    # out here too.
    add(a, b)

    # Copies the contents of b into the memory allocated for a
    a <- b

    # Does an in-place swap of the contents of a and b
    swap a b

## `require`

Libraries can be loaded via `require`.  If the target platform has no library,
then compilation will fail.

Things like floating point, USART, I2C, Timers, DAC, PWM, PID/Math Accelerator,
&c support will require the library to be imported. For source libraries,
only require code/functions will be in the final output.

## Types of Types

There are two types of type: heap allocated and simple. Heap allocated types
cannot (in general) be represented in registers or on the stack. Heap allocated
types are passed-by-reference

Default, always available types are

* nibble
* byte
* boolean
* int8
* int16
* Array (fixed-size)
* LessThan{value}
* GreaterThan{value}

Note that floating point types are not always available.  Support would
require a `require floating_point` assertion.

### No Dynamic Allocation

There is no way to dynamically allocate memory. All variables must be of
a known size at compile time and the compiler will figure out how to
best allocate memory then.

### Byte <=> Type Isomorphism

All types must map back to some size of bytes at compile time, which will be
allocated on the heap if more than 2 bytes.

    byte  = 1 byte
    int8  = 1 byte
    int16 = 2 bytes

    Packet := byte[6] = 6 bytes

    TwoPacket:
      Packet a
      Packet b
                 =  12 bytes # all allocations are sequential

    AB:
      int8  a
      int16 b
                 = 3 bytes

As such, the maximum amount of memory needed for any function call should
be able to be known at compile time.


Individual bytes can be set or manipulated via the `@` operator:

    ab <= AB (allocates (at compile time) 3 bytes in the heap)
    p@0 <= 0x01 # Sets the first byte to 0x01
    p@1 <= 0x02 # Sets the second byte to 0x02
    p@2 <= 0x03 # Sets the third byte to 0x03

    # ab.a == 1
    # ab.b == 515

## `LessThan` and `GreaterThan`

The value on the right of the `@` _must_ be less than the size of the object.
If a literal, this is checked at compile-time. If not, it must be of type
`LessThan{size}` (above, `LessThan{3}`) which can be a variable declared as
such, and when incremented or set some additional math is done to clean it
up. Example:

    x <= LessThan{sizeof{TwoPacket}}(0)
    x++

would roughly become something like, since it's an increment (or simple
addition of 2 `LessThan{x}` values):

    LDI  r16, 0
    INC  r16
    CPI  r16, 12
    BRCC after
    SUBI r16, 12
    after: 

however, for an arbitrary set

    x <= LessThan{sizeof{TwoPacket}}(0)
    x <= UDR0

would become something like:

    LDI r16, 0
    LDS r16, UDR0
    loop:
    CPI  r16, $0C
    BRCC after
    SUBI r16, $0C
    BRCC loop
    after:


## Annotations and Budgets

A method can be annotated with notes to the compiler to error if a condition
isn't met, such as max memory used or max cycles to execute. (Something like
a "Language Server" or IDE in general should be able to extract the current
usage of the budget from the compiler as well.

    @budget cycles 6
    def hello():
      x <= LessThan{sizeof{TwoPacket}}(0)
      x++
      return x

will pass (using the entire budget (right now it's naïve and will count `BRCC` as 2 cycles)), but

    @budget cycles 5
    def hello():
      x <= LessThan{sizeof{TwoPacket}}(0)
      x <= UDR0
      return x

will fail as it could require up to 129 cycles (if UDR0 was, say, 255)

## Transactions

Transactions are code where interrupts are turned off.

    def hello():
      transaction:
        x <= LessThan{sizeof{TwoPacket}}(0)
        return x

would give something like

    CLI
    LDI r16, $00
    SEI

## Tasks and Interrupts

### Tasks

Tasks are functions with two parts, `setup` and `body`. In `setup`, all
allocations must happen. All `setup`s for all tasks will be run before any
`body` is executed. The `body` of each task will be executed in a loop.
Execution of `body` will start at the beginning unless it had `yeild`ed.

### Interuppts

Interrupts are similar to tasks, but not executed in a loop, but when they
the interrupt happens.

### Table Definitions

Sometimes it makes sense to define a function by a table. Imagine if you will
a garage door. It opens when you hit the button, closes when you hit the
button, and opens when the sensor is triggered and it's closing.

    enum States := nibble:
      Open             := 0x0
      Opening          := 0x1
      Opening_Finished := 0x6
      Opening_Started  := 0x8
      Closed           := 0x2
      Closing          := 0x3
      Closing_Finished := 0x7
      Closing_Started  := 0x9
      Error            := 0x4
      Stopped          := 0x5

    enum Input := nibble:
      Button              := 0x0
      Obstical_Sensor     := 0x1
      Closed_Limit_Switch := 0x2
      Opened_Limit_Switch := 0x3
      No_Input            := 0x4

    table transition(States state, Input input) => States:
      | state            | input               | return           |
      | ----------       | --------            | ----------       |
      | Open             | Button              | Closing_Started  |
      | Open             | Obstical_Sensor     | Open             |
      | Open             | Closed_Limit_Switch | Error            |
      | Open             | Opened_Limit_Switch | Error            |
      | Open             | No_Input            | Open             |

      | Opening          | Button              | Stopped          |
      | Opening          | Obstical_Sensor     | Opening          |
      | Opening          | Closed_Limit_Switch | Error            |
      | Opening          | Opened_Limit_Switch | Opening_Finished |
      | Opening          | No_Input            | Opening          |

      | Opening_Finished | -                   | Open             |

      | Opening_Started  | -                   | Opening          |

      | Closed           | Button              | Opening_Started  |
      | Closed           | Obstical_Sensor     | Closed           |
      | Closed           | Closed_Limit_Switch | Error            |
      | Closed           | Opened_Limit_Switch | Error            |
      | Closed           | No_Input            | Closed           |

      | Closing          | Button              | Stopped          |
      | Closing          | Obstical_Sensor     | Stopped          |
      | Closing          | Closed_Limit_Switch | Closing_Finished |
      | Closing          | Opened_Limit_Switch | Error            |
      | Closing          | No_Input            | Closing          |

      | Closing_Finished | -                   | Closed           |

      | Closing_Started  | -                   | Closing          |

      | Error            | Button              | Opening          |
      | Error            | -                   | Error            |

      | Stopped          | Button              | Opening          |
      | Stopped          | Obstical_Sensor     | Stopped          |
      | Stopped          | No_Input            | Stopped          |
      | Stopped          | -                   | Error            |

## Match

Using the example above, we can look at how matching works.  Matches need to be
exhusive; the following will error:

    loop:
      input <= read_input()
      current_state <= transition(current_state, input)

      match current_state:
        case States.Opening_Started:
          start_motor_pulling_up()
          turn_light_on()
        case States.Opening_Finished:
          stop_motor()
          turn_light_off()

        case States.Closing_Started:
          start_motor_pulling_down()
          turn_light_on()
        case States.Closing_Finished:
          stop_motor()
          turn_light_off()

        case States.Error:
          blink_light()

However, we can add a default match:

    loop:
      input <= read_input()
      current_state <= transition(current_state, input)

      match current_state:
        case States.Opening_Started:
          start_motor_pulling_up()
          turn_light_on()
        case States.Opening_Finished:
          stop_motor()
          turn_light_off()

        case States.Closing_Started:
          start_motor_pulling_down()
          turn_light_on()
        case States.Closing_Finished:
          stop_motor()
          turn_light_off()

        case States.Error:
          blink_light()

        else:
          pass

## Macros

I'm still working out exactly how macros should behave and work. I think
I'm going to play around with Common Lisp, Rust, and maybe Nim macros.
Some initial thoughts can be seen in sample-002.

## Pattern Parameter Matching

### Array/Slice

`Array`s are what can be declared as variables. `Slice`s are what is used
for function parameters. Slice is explicetly calling out that this parameter
is an array, but not an array that you declared? I'm working on it.

The syntax for a Slice parameter can include that multiple items being 
extracted from the Slice being passed in; one of the extracted parameters
may be prefixed with an @ symbol, symbolizing where the the rest of the
slice being passed in, that is the elements not being extracted. 
For example: `[1,2,3,4]` passed into:

    [x,@rest]         => x=1, rest=[2,3,4]
    [@rest,x]         => x=4, rest=[1,2,3]
    [x,y,@rest]       => x=1, y=2, rest=[3,4]
    [x,@rest,y]       => x=1, y=4, rest=[2,3]
    [w,x,y,z,@rest]   => w=1, x=2, y=3, z=4, rest=[]
    [w,x,y,z,a,@rest] => compiler error

However, you cannot create a new slice from non-adjacent extracts. This is
allowed:

    func a(Slice{T} [a,b,@c]):
      a([a,b])
      a([b,@c])

but this is not:

    func a(Slice{T} [a,b,@c]):
      a([a,@c])

You'll need to have an array allocated and assigned to.

This may also be used in a `match`. However `match`es need to be exhustive,
for instance the following won't compile:

    func a(Slice{T} b):
      match b:
        [a,b,@c]:
          a([a,b])
          a([b,@c])

however, this will:

    func a(Slice{T} b):
      match b:
        [a,b,@c]:
          a([a,b])
          a([b,@c])
        [a, @c]:
          a([a])
          a([@c)
        [] -> pass

Some example usage:

    # So, what we're doing here for bubble short, is to take an array, extracted 
    # the last element, partially sort the whole array, including the extracted
    # element. We then do this again, without the extracted element. If we
    # have no elements in the rest of the slice, then we terminate.
    def bubble_sort{T := Comparable, S := Slice{T}}(mut S array):
        match array:
          [@rest, x]:
            bubble_partial_sort([rest, x])
            bubble_sort(rest)
          [] -> pass

    # This function partially sort the passed in slice by extracting the last
    # two elements, swapping them if nessecary. Swap happens in-place, so
    # we can then partially sort the remainer of the slice by passing in
    # the rest prepended to the first extracted value. (Values can only be
    # concatented in the order extracted: rest;y is a compiler error below.
    def bubble_partial_sort{T := Comparable, S := Slice{T}}(mut S array):
      match array:
        [@rest, x, y]:
          if x > y:
            swap x y
          bubble_partial_sort([rest,x])
        [@rest, x] -> pass
        [] -> pass

    # Since slice extracts act like references, assigning to them
    # will change the value in the array.
    def void double{T := Addable, A := Slice<size_a>{T}, B := Slice<size_b>{T}; size_b >= size_a}(A a, mut B b):
      match a, b:
        [x, @xs], [y, @ys]:
          y <= x + x
          double(xs, ys)
        [], [y, @ys] -> pass
        [], [] -> pass

    # Reduce the array by extracting the first element, adding it to the 
    # carry. If there is nothing left to recurse on, we return the
    # carry.
    def T sum{T := Addable, S := Slice{T}}(S array, T carry):
      return match array:
        [x,@xs] -> return sum(xs, carry + x)
        [] -> return carry

Since these can be tail-call optimized, the compiler will be able to
produce decent code for this without requiring lots of stack space.

Part of the rationale for this is avoiding a looping construct. I'm just
not a fan of loops and find they're easy to get wrong. If you don't use
array indecies, you can't have off-by-one errors.

### Records

A similar thing can be done for records. A record can be followed by an
expression that will extract fields (and potentially not all fields) into
function-local variables. I'm still debating this one, but I think it's
neat.

    record Vector:
      int8 x
      int8 y

    func add(Vector {x x1, y y1}, Vector {x x2, y y2}) => Vector:
      return Vector { x <- x1 + x2, y <- y1 + y2 }

## Traits

Traits are a way of defining composable functionality. `record`s are
simple structures in memory and contain no function definitions on them.
Traits allow one to define functionality on `record`s, similar to how
it's done in rust. This is not inhereitence in the normal
object-oriented way -- there are no parents or base classes; the
closest description is that traits are similar to interfaces, if
intefaces can't have a parent. 

To define a trait, you list the methods it has, and then you can implement
if for a type.

  record Point:
    int8 x
    int8 y

  trait Addable{S,T}:
    op +(S a, T b)
    op -(S a, T b)

  trait Comparable{T}:
    op <(T a, T b)

  impl Addable{S := Point, T := Point}:
    op +(S a, T b):
      return Point {x <- a.x + b.x, y <- a.y + b.y}
    op -(S a, T b):
      return Point {x <- a.x - b.x, y <- a.y - b.y}

  # This isn't the best way to compare points...but it's a way?
  impl Comparable{Point}:
    op <(Point a, Point b):
      return a.x < b.x || a.y < b.y

To constrain traits on a function parameter, use `;`:

  func do_stuff{T := Addable;Comparable}(T a, T b):
    pass

notice how the constraints are defined before the parameter list, not
inside.
