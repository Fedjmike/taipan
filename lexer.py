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
      
    def error(self, msg):
        self.error_function(msg)
        
    def next_char(self):
        self.char = self.text[self.char_no]
        
    def eat_char(self):
        ch = self.char
        self.token.add_char(self.char)
        self.next_char()
        return ch
        
    def skip_meaningless_whitespace(self):
        while self.char in " \t":
            self.next_char()
            
    def indentation(self):
        indent_char = None
        indent_count = 0
        
        while self.char in " \t":
            indent_char = self.char
            indent_count = 0
            
            while self.char == indent_char:
                self.next_char()
                indent_count += 1
                
            if self.char in " \t":
                self.error("Mixed indentation characters")
                
            if self.char == "\r":
                self.next_char()
                
            else:
                break
                
        if indent_char is None:
            pass
        
        elif self.indent_char is None:
            self.indent_char = indent_char
            self.indent_multiple = indent_count
        
        elif self.indent_char != indent_char:
            self.error("Wrong indentation character")
            
        return indent_count / self.indent_multiple
        
    def next(self):
        if self.token.type = TokenType.EndOfLine or self.token is None:
            cur_indent_level = self.indentation()
            
            self.outstanding_indent_difference =
                cur_indent_level - self.indent_level
            self.indent_level = cur_indent_level
            
        if self.outstanding_indent_difference > 0:
            self.outstanding_indent_difference -= 1
            return Token(TokenType.StartOfBlock)
            
        elif self.outstanding_indent_difference < 0:
            self.outstanding_indent_difference += 1
            return Token(TokenType.EndOfBlock)
    
        self.token = Token(TokenType.Unknown)
        
        self.skip_meaningless_whitespace()
        
        if self.char in "\r":
            self.token.type = TokenType.EndOfLine
            self.next_char()
    
        elif self.char.isnumeric():
            while self.char.isalpha():
                self.eat_char()
                
            self.token.type = TokenType.NumLit
    
        elif self.char.isalpha():
            while self.char.isalpha():
                self.eat_char()
                
            self.token.type =
                TokenType.Keyword if self.token.str in self.keywords
                else TokenType.Ident
        
        elif self.char in self.operators:
            self.token.type = TokenType.Op
            first_char = self.eat_char()
            
            if first_char + self.char in self.operators:
                self.eat_char()
                
        elif self.char in "\"'":
            self.token.type = TokenType.StrLit
            quote = self.eat_char()
            
            while self.waiting_for(quote):
                self.eat_char()
                
            self.eat_char()
            
        return token
        
    def see(self, str):
        return self.token.str == str
        
    def match(self, str):
        if self.see(str):
            self.next()
            
        else:
            self.error("Expected '%s', found '%s'" % (str, self.token.str))
        
    def try_match(self, str):
        if self.see(str):
            self.next()
            return True
            
        else:
            return False
        
    def match_type(self, _type):
        if self.token.type == _type:
            self.next():
        
        else:
            self.error("Expected %s, found '%s'" % (_type.name, self.token.str))