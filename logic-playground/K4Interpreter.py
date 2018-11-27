from K4AST import *

def unify(values, expression):
    if isinstance(expression, ConstraintExpression):
        lhs = expression.lhs
        if isinstance(lhs, ConstraintExpression):
            lhs = unify(values, lhs)

        rhs = expression.rhs
        if isinstance(rhs, ConstraintExpression):
            rhs = unify(values, rhs)


            
