class ConstraintCall:
    def __init__(self, name, params):
        self.name = name
        self.params = params

class ConstraintExpression:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    def format(self, indent = ""):
        return indent + self.op + "(" + str(self.lhs) + ", " + str(self.rhs) + ")"
    def __str__(self):
        return self.format()

class ConstraintRule:
    def __init__(self, name, params, expression):
        self.name = name
        self.params = params
        self.expression = expression
        self.assign_free_bound(self.expression)

    def assign_free_bound(self, expression):
        if isinstance(expression, Term):
            if expression.name in self.params:
                return BoundTerm(expression.name)
            else:
                return FreeTerm(expression.name)
        elif isinstance(expression, ConstraintExpression):
            expression.lhs = self.assign_free_bound(expression.lhs)
            expression.rhs = self.assign_free_bound(expression.rhs)
        return expression
    def format(self, indent = ""):
        return indent + "ConstraintRule(" + self.name + ")(" + ",".join(self.params) + ") := " + self.expression.format()
    def __str__(self):
        return self.format()

class ConstraintRules:
    def __init__(self, rules):
        self.rules = rules
    def format(self, indent = ""):
        return ("\n"+indent).join([x.format(indent) for x in self.rules])
    def __str__(self):
        return self.format()

class Atom:
    def __init__(self, name):
        self.name = name.replace("'", "")
    def format(self, indent = ""):
        return indent + "Atom(" + self.name + ")"
    def __str__(self):
        return self.format()

class Module:
    def __init__(self, name, constraint_rules, facts):
        self.name = name
        self.constraint_rules = constraint_rules
        self.facts = facts
    def format(self, indent = ""):
        return indent + "Module " + self.name + "\n" + \
                self.constraint_rules.format(indent + "\t") + "\n" + \
                self.facts.format(indent+"\t")
    def __str__(self):
        return self.format()

class Term:
    def __init__(self, name):
        self.name = name
    def format(self, indent = ""):
        return indent + "Term(" + self.name + ")"
    def __str__(self):
        return self.format()

class FreeTerm:
    def __init__(self, name):
        self.name = name
    def format(self, indent = ""):
        return indent + "FreeTerm(" + self.name + ")"
    def __str__(self):
        return self.format()

class BoundTerm:
    def __init__(self, name):
        self.name = name
    def format(self, indent = ""):
        return indent + "BoundTerm(" + self.name + ")"
    def __str__(self):
        return self.format()

class Assignment:
    def __init__(self, term, value):
        self.term = term
        self.value = value
    def format(self, indent = ""):
        return indent + "Assign(" + self.term + ", " + str(self.value) + ")"
    def __str__(self):
        return self.format()

class Fact:
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms
    def format(self, indent = ""):
        return indent + "Fact(" + self.name + ", (" + ", ".join([str(x) for x in self.terms]) +  "))"
    def __str__(self):
        return self.format()

class Facts:
    def __init__(self, facts):
        self.facts = facts
    def format(self, indent = ""):
        return indent + ("\n"+indent).join([x.format() for x in self.facts])
    def __str__(self):
        return self.format()

class Variable:
    def __init__(self, name):
        self.name = name
    def format(self, indent = ""):
        return indent + "Variable(" + self.name +  ")"
    def __str__(self):
        return self.format()

class Number:
    def __init__(self, value):
        self.value = value
    def format(self, indent = ""):
        return indent + "Number(" + str(self.value) +  ")"
    def __str__(self):
        return self.format()

