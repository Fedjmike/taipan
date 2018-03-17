class Ast:
    pass


class AstIdent(Ast):
    def __init__(self, ident):
        self.ident = ident


class AstSum(Ast):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AstFnDef(Ast):
    def __init__(self, name, arguments, body_statements):
        self.name = name
        self.arguments = arguments
        self.body_statements = body_statements


class AstReturn(Ast):
    def __init__(self, expr):
        self.expr = expr


class AstFnCall(Ast):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class AstLet(Ast):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AstIf(Ast):
    def __init__(self, condition, if_body_statements, else_body_statements):
        self.condition = condition
        self.if_body_statements = if_body_statements
        self.else_body_statements = else_body_statements


class AstWhile(Ast):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
