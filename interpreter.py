import AST
from visit import *
import openpyxl

database_name = "database.xlsx"


def insert_columns(sheet, row, rownum):
    for i in range(len(row)):
        sheet.cell(row=rownum, column=i+1).value = row[i]


def insert_row(sheet, row, rownum):
    if rownum == 2:
        id = 1
    else:
        id = sheet.cell(row=rownum-1, column=1).value +1
    row = [id] + row
    for i in range(len(row)):
        sheet.cell(row=rownum, column=i+1).value = row[i]


def read_row(sheet, rownum):
    row = sheet[rownum]
    return [cell.value for cell in row]


def modify_row(columns, row):
    modified_row = {}
    for colnum, column in enumerate(columns):
        modified_row[column] = row[colnum]
    return modified_row


class Interpreter(object):
    current_row = None

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

    @when(AST.Create_Table)
    def visit(self, node):
        table_name = self.visit(node.table)
        columns = self.visit(node.columns)

        database = openpyxl.load_workbook(database_name)
        if table_name in database.get_sheet_names():
            table = database.get_sheet_by_name(table_name)
            database.remove_sheet(table)
        table = database.create_sheet(table_name)
        insert_columns(table, columns, 1)

        database.save(database_name)

    @when(AST.Insert_Into)
    def visit(self, node):
        table_name = self.visit(node.table)
        columns = self.visit(node.columns)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)
        insert_row(table, columns, table.max_row+1)

        database.save(database_name)

    @when(AST.Select_From)
    def visit(self, node):
        columns = self.visit(node.columns)
        table_name = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)
            selected_row = [modified_row[column] for column in columns]
            print(selected_row)

    @when(AST.Select_From)
    def visit(self, node):
        columns = self.visit(node.columns)
        table_name = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        for rownum in range(2, table.max_row+1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)
            selected_row = [modified_row[column] for column in columns]
            print(selected_row)

    @when(AST.Select_From_Where)
    def visit(self, node):
        columns = self.visit(node.columns)
        table_name = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)
            selected_row = [modified_row[column] for column in columns]
            Interpreter.current_row = modified_row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                print(selected_row)


    @when(AST.Columns)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left + right

    @when(AST.Column)
    def visit(self, node):
        return [node.name]

    @when(AST.Table)
    def visit(self, node):
        return node.name

    @when(AST.Condition)
    def visit(self, node):
        left = self.visit(node.left)
        op = node.op
        right = self.visit(node.right)
        if op == "==":
            return Interpreter.current_row[left] == right
        if op == "!=":
            return Interpreter.current_row[left] != right

    @when(AST.ID)
    def visit(self, node):
        return node.name

    @when(AST.STRING)
    def visit(self, node):
        return str(node.value)

    @when(AST.NUMBER)
    def visit(self, node):
        return float(node.value)
