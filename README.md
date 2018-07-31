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

## Types of Types

There are two types of type: heap allocated and simple. Heap allocated types
cannot (in general) be represented in registers or on the stack. Heap allocated
types are passed-by-reference

### No Dynamic Allocation
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

### Byte <=> Type Isomorphism

Individual bytes can be set or manipulated via the `@` operator:

    ab <= AB (allocates (at compile time) 3 bytes in the heap)
    p@0 <= 0x01 # Sets the first byte to 0x01
    p@1 <= 0x02 # Sets the second byte to 0x02
    p@2 <= 0x03 # Sets the third byte to 0x03

    # ab.a == 1
    # ab.b == 515

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
