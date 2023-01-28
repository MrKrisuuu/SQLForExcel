from scanner import lexer
from parser import parser


if __name__ == '__main__':
    filename = "selects.sql"
    file = open(filename, "r")

    parser = parser
    text = file.read()
    parser.parse(text, lexer=lexer)