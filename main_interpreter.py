from scanner import lexer
from parser import parser
from interpreter import Interpreter
from TreePrinter import TreePrinter

if __name__ == '__main__':
    filename = "SQL.txt"
    file = open(filename, "r")

    text = file.read()
    ast = parser.parse(text, lexer=lexer)

    ast.accept(Interpreter())

