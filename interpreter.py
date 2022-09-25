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
        if not isinstance(columns, list):
            columns = [columns]

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
        variables = self.visit(node.variables)
        if not isinstance(variables, list):
            variables = [variables]

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)
        insert_row(table, variables, table.max_row+1)

        database.save(database_name)

    @when(AST.Update)
    def visit(self, node):
        table_name = self.visit(node.table)
        sets = self.visit(node.sets)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)

            Interpreter.current_row = modified_row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                for (column_name, value) in sets:
                    i = columns_name.index(column_name)
                    table.cell(row=rownum, column=i+1).value = value

        database.save(database_name)

    @when(AST.Delete_From)
    def visit(self, node):
        table_name = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        dels = 0
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum-dels)
            modified_row = modify_row(columns_name, row)

            Interpreter.current_row = modified_row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                table.delete_rows(rownum-dels, 1)
                dels += 1

        database.save(database_name)

    @when(AST.Select_From)
    def visit(self, node):
        columns = self.visit(node.columns)
        table_name = self.visit(node.table)
        if not isinstance(columns, list):
            columns = [columns]

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)

        indices = [i for i, x in enumerate(columns) if x == "*"]
        for index in reversed(indices):
            columns[index:index+1] = columns_name

        for rownum in range(2, table.max_row+1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)
            selected_row = [modified_row[column] for column in columns]
            print(selected_row)

    @when(AST.Select_From_Where)
    def visit(self, node):
        columns = self.visit(node.columns)
        table_name = self.visit(node.table)
        if not isinstance(columns, list):
            columns = [columns]

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

    @when(AST.Sets)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left + right

    @when(AST.Set)
    def visit(self, node):
        column = self.visit(node.column)
        variable = self.visit(node.variable)
        return [(column, variable)]

    @when(AST.Columns)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.right, AST.Columns):
            return [left] + right
        else:
            return [left] + [right]

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

    @when(AST.Variables)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.right, AST.Variables):
            return [left] + right
        else:
            return [left] + [right]

    @when(AST.STRING)
    def visit(self, node):
        return str(node.value)

    @when(AST.NUMBER)
    def visit(self, node):
        return float(node.value)
