from scanner import lexer
from parser import parser
from TreePrinter import TreePrinter

if __name__ == '__main__':
    filename = "selects.sql"
    file = open(filename, "r")

    text = file.read()
    ast = parser.parse(text, lexer=lexer)
    ast.printTree()