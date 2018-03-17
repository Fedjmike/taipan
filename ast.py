class Ast:
    pass


class Ident(Ast):
    def __init__(self, ident):
        self.ident = ident


class Sum(Ast):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class FnDef(Ast):
    def __init__(self, name, arguments, body_statements):
        self.name = name
        self.arguments = arguments
        self.body_statements = body_statements


class Return(Ast):
    def __init__(self, expr):
        self.expr = expr


class FnCall(Ast):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class Let(Ast):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class If(Ast):
    def __init__(self, condition, if_body_statements, else_body_statements):
        self.condition = condition
        self.if_body_statements = if_body_statements
        self.else_body_statements = else_body_statements


class While(Ast):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
