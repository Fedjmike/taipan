from lexer import TokenType
import ast


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def statement(self):
        if self.lexer.see("def"):
            return self.def_statement()

        elif self.lexer.try_match("return"):
            node = ast.Return(self.expr())
            self.lexer.match_type(TokenType.EndOfLine)
            return node

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
        while self.lexer.waiting_for_type(TokenType.EndOfBlock):
            body_statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        return ast.FnDef(name, arguments, body_statements)

    def let(self):
        self.lexer.match("let")
        name = self.lexer.match_type(TokenType.Ident)
        self.lexer.match("=")
        value = self.expr()

        return ast.Let(name, value)

    def if_statement(self):
        node = ast.If()

        self.lexer.match("if")
        node.condition = self.expr()
        self.lexer.match(":")
        self.lexer.match_type(TokenType.StartOfBlock)
        self.lexer.match_type(TokenType.EndOfLine)

        while self.lexer.waiting_for_type(TokenType.EndOfBlock):
            node.if_body_statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        if self.lexer.try_match("else"):
            self.lexer.match(":")
            self.lexer.match_type(TokenType.EndOfLine)
            self.lexer.match_type(TokenType.StartOfBlock)

            while self.lexer.waiting_for_type(TokenType.EndOfBlock):
                node.else_body_statements.append(self.statement())
            self.lexer.next()  # Pass through EndOfBlock

        return node

    def while_loop(self):
        self.lexer.match("while")
        condition, statements = self.expr(), []
        self.lexer.match(":")
        self.lexer.match_type(TokenType.EndOfLine)
        self.lexer.match_type(TokenType.StartOfBlock)

        while self.lexer.waiting_for_type(TokenType.EndOfBlock):
            statements.append(self.statement())
        self.lexer.next()  # Pass through EndOfBlock

        return ast.While(condition, statements)

    def expr(self):
        return self.sum()

    def sum(self):
        left = self.factor()

        if self.lexer.try_match("+"):
            return ast.Sum(left, self.expr())

        else:
            return left

    def factor(self):
        ident = self.lexer.match_type(TokenType.Ident)

        if self.lexer.try_match("("):

            arguments = []
            if not self.lexer.try_match(")"):
                while True:
                    arguments.append(self.expr())

                    if not self.lexer.try_match(","):
                        break

            self.lexer.match(")")
            return ast.FnCall(ident, arguments)

        else:
            return ast.Ident(ident)
