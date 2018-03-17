import sys

from parse import Parser
from lexer import Lexer

def main():
    def error_printer(msg):
        print(msg)

    filename = sys.argv[1]
    
    with open(filename) as file:
        text = file.read()
        print(text)
        
    Parser(Lexer(text, error_printer)).parse()
    

if __name__ == "__main__":
    main()