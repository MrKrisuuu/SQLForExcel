from pathlib import Path
from scanner import lexer
from parser import parser
from interpreter import Interpreter
import openpyxl


class Manager:
    def __init__(self, name):
        self.name = name + ".xlsx"
        my_file = Path(self.name)
        if not my_file.exists():
            database = openpyxl.Workbook()
            sheet = database.get_sheet_by_name("Sheet")
            sheet.title = "Basic stuff"
            database.save(self.name)

    def execute(self, sql_query):
        ast = parser.parse(sql_query, lexer=lexer)
        return ast.accept(Interpreter(self.name))
