from lexer import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def statement(self):
        if self.lexer.see("def"):
            return self.def_statement()

        elif self.lexer.see("if"):
            return self.if_statement()

        elif self.lexer.see("while"):
            return self.while_loop()

        elif self.lexer.see("let"):
            node = self.let()
            self.lexer.match_type(TokenType.EndOfLine)
            return node

        else:
            node = self.expr()
            self.lexer.match_type(TokenType.EndOfLine)
            return node

    def def_statement(self):
        self.lexer.match("def")
        name = self.lexer.match_type(TokenType.Ident)
        self.lexer.match("(")

        arguments = []
        if not self.lexer.try_match(")"):
            while True:
                arguments.append(self.lexer.match_type(TokenType.Ident))

                if not self.lexer.try_match(","):
                    break

        self.lexer.match(")")
        self.lexer.match(":")

        self.lexer.match_type(TokenType.EndOfLine)
        self.lexer.match_type(TokenType.StartOfBlock)

        body_statements = []
        while self.lexer.token.type != TokenType.EndOfBlock():
            body_statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        return AstFnDef(name, arguments, body_statements)

    def let(self):
        self.lexer.match("let")
        name = self.lexer.match_type(TokenType.Ident)
        self.lexer.match("=")
        value = self.expr()

        return AstLet(name, value)

    def if_statement(self):
        node = AstIf()

        self.lexer.match("if")
        node.condition = self.expr()
        self.lexer.match(":")
        self.lexer.match_type(TokenType.StartOfBlock)
        self.lexer.match_type(TokenType.EndOfLine)

        while self.lexer.token.type != TokenType.EndOfBlock():
            node.if_body_statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        if self.lexer.try_match("else"):
            self.lexer.match(":")
            self.lexer.match_type(TokenType.EndOfLine)
            self.lexer.match_type(TokenType.StartOfBlock)

            while self.lexer.token.type != TokenType.EndOfBlock:
                node.else_body_statements.append(self.statement())
            self.lexer.next()  # Pass through EndOfBlock

        return node

    def while_loop(self):
        self.lexer.match("while")
        condition, statements = self.expr(), []
        self.lexer.match(":")
        self.lexer.match_type(TokenType.EndOfLine)
        self.lexer.match_type(TokenType.StartOfBlock)

        while self.lexer.token.type != TokenType.EndOfBlock:
            statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        return AstWhile(condition, statements)

    def expr(self):
        return self.sum()

    def sum(self):
        left = self.lexer.match_type(TokenType.Ident)

        if not self.lexer.try_match("+"):
            return AstIdent(left)
        else:
            return AstSum(left, self.sum())


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
