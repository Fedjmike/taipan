from enum import Enum

class TokenType(Enum):
    Unknown = 0
    Keyword = 1
    Ident = 2
    Op = 3
    NumLit = 4
    StrLit = 5
    StartOfBlock = 6
    EndOfBlock = 7
    EndOfLine = 8
    EndOfFile = 9
    
class Token:
    def __init__(self, _type):
        self.str = ""
        self.type = _type
        
    def add_char(self, char):
        self.str += char

class Lexer:
    def __init__(self, text, error_printer):
        self.error_printer = error_printer
        self.text = text
        
        self.token = None
        
        self.char_no = 0
        self.char = None
        
        self.indent_char = None
        self.indent_multiple = None
        
        self.indent_level = 0
        self.outstanding_indent_difference = 0
        
        self.keywords = ["def", "class", "if", "else", "elif", "for", "while", "break", "return", "not"]
        self.operators = [":", "(", ")", "[", "]", "{", "}",
                          "=", "+", "-", "*", "/"]
                      
        self.next_char()
        self.next()
      
    def error(self, msg):
        self.error_printer(msg)
        
    def next_char(self):
        try:
            self.char = self.text[self.char_no]
            self.char_no += 1
            
        except IndexError:
            self.char = None
        
    def eat_char(self):
        if self.char is None:
            return
            
        ch = self.char
        self.token.add_char(self.char)
        self.next_char()
        return ch
        
    def skip_meaningless_whitespace(self):
        while self.char in [" ", "\t"]:
            self.next_char()
            
    def indentation(self):
        indent_char = None
        indent_count = 0
        
        while self.char in [" ", "\t"]:
            indent_char = self.char
            indent_count = 0
            
            while self.char == indent_char:
                self.next_char()
                indent_count += 1
                
            if self.char in " \t":
                self.error("Mixed indentation characters")
                
            if self.char == "\n":
                self.next_char()
                
            else:
                break
                
        if indent_char is None:
            return 0
        
        else:
            if self.indent_char is None:
                self.indent_char = indent_char
                self.indent_multiple = indent_count
            
            elif self.indent_char != indent_char:
                self.error("Wrong indentation character")
            
            return indent_count / self.indent_multiple
        
    def next(self):
        if self.token is None or self.token.type == TokenType.EndOfLine:
            cur_indent_level = self.indentation()
            
            self.outstanding_indent_difference = \
                cur_indent_level - self.indent_level
            self.indent_level = cur_indent_level
            
        if self.outstanding_indent_difference > 0:
            self.outstanding_indent_difference -= 1
            self.token = Token(TokenType.StartOfBlock)
            return
            
        elif self.outstanding_indent_difference < 0:
            self.outstanding_indent_difference += 1
            self.token = Token(TokenType.EndOfBlock)
            return
    
        self.token = Token(TokenType.Unknown)
        
        self.skip_meaningless_whitespace()
        
        if self.char is None:
            self.token.type = TokenType.EndOfFile
        
        elif self.char in "\n":
            self.token.type = TokenType.EndOfLine
            self.next_char()
    
        elif self.char.isnumeric():
            while self.char.isalpha():
                self.eat_char()
                
            self.token.type = TokenType.NumLit
    
        elif self.char.isalpha():
            while self.char.isalpha():
                self.eat_char()
                
            self.token.type = \
                TokenType.Keyword if self.token.str in self.keywords \
                else TokenType.Ident
        
        elif self.char in self.operators:
            self.token.type = TokenType.Op
            first_char = self.eat_char()
            
            if first_char + self.char in self.operators:
                self.eat_char()
                
        elif self.char in "\"'":
            self.token.type = TokenType.StrLit
            quote = self.eat_char()
            
            while self.char not in [quote, None]:
                self.eat_char()
                
            self.eat_char()
        
    def see(self, str):
        return self.token.str == str
        
    def see_type(self, _type):
        return self.token.type == _type
        
    def waiting_for_type(self, _type):
        return self.token.type not in [TokenType.EndOfFile, _type]
        
    def match(self, str):
        if self.see(str):
            self.next()
            
        else:
            self.error("Expected '%s', found %s '%s'" % (str, self.token.type.name, self.token.str))
            
    def try_match(self, str):
        if self.see(str):
            self.next()
            return True
            
        else:
            return False
        
    def match_type(self, _type):
        if self.token.type == _type:
            self.next()
        
        else:
            self.error("Expected %s, found %s '%s'" % (_type.name, self.token.type.name, self.token.str))
