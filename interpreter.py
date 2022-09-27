import AST
from visit import *
import openpyxl

database_name = "database.xlsx"


def insert_first_row(sheet, row, rownum):
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


def read_first_row(sheet, shortname):
    row = sheet[1]
    data = {}
    for (i, cell) in enumerate(row):
        data[shortname + "." + cell.value] = i
    return data


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
        insert_first_row(table, columns, 1)

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

    @when(AST.Select_From)
    def visit(self, node):
        # SELECT
        columns_select = self.visit(node.columns)
        if not isinstance(columns_select, list):
            columns_select = [columns_select]

        # FROM
        (table_full, table_short) = self.visit(node.table)
        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_full)

        columns_name = read_first_row(table, table_short)

        res = []
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(list(columns_name.keys()), row)
            res.append(modified_row)

        # JOIN ON
        joinings = self.visit(node.joining)
        if joinings is not None:
            for ((table_full, table_short), condition_node) in joinings:
                table = database.get_sheet_by_name(table_full)
                columns_name = read_first_row(table, table_short)
                join = []
                for rownum in range(2, table.max_row + 1):
                    row = read_row(table, rownum)
                    modified_row = modify_row(list(columns_name.keys()), row)
                    join.append(modified_row)
                new_res = []
                for res_row in res:
                    for join_row in join:
                        new_row = res_row | join_row
                        Interpreter.current_row = new_row
                        condition = self.visit(condition_node)
                        Interpreter.current_row = None
                        if condition:
                            new_res.append(new_row)
                res = new_res

        # WHERE
        new_res = []
        for row in res:
            Interpreter.current_row = row
            condition = self.visit(node.whering)
            Interpreter.current_row = None
            if condition is None:
                new_res.append(row)
            elif condition:
                new_res.append(row)
        res = new_res

        # ORDER BY
        ordering = self.visit(node.ordering)
        if ordering is not None:
            for column in reversed(ordering):
                res.sort(key=lambda x: x[columns_name[column]])

        # RETURN
        for row in res:
            line = []
            for col in columns_select:
                if col == "*":
                    line += list(row.values())
                else:
                    line += row[col]
            print(line)

    @when(AST.Join_On)
    def visit(self, node):
        table = self.visit(node.table)
        return [(table, node.condition)]

    @when(AST.Where)
    def visit(self, node):
        return self.visit(node.condition)

    @when(AST.Order_By)
    def visit(self, node):
        columns = self.visit(node.columns)
        if not isinstance(columns, list):
            columns = [columns]
        return columns

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
                    table.cell(row=rownum, column=i + 1).value = value

        database.save(database_name)

    @when(AST.Delete_From)
    def visit(self, node):
        table_name = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(table_name)

        columns_name = read_row(table, 1)
        dels = 0
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum - dels)
            modified_row = modify_row(columns_name, row)

            Interpreter.current_row = modified_row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                table.delete_rows(rownum - dels, 1)
                dels += 1

        database.save(database_name)

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

    @when(AST.Table)
    def visit(self, node):
        full = self.visit(node.full)
        short = self.visit(node.short)
        return (full, short)

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
        if isinstance(node.right, AST.ID):
            if op == "==":
                return Interpreter.current_row[left] == Interpreter.current_row[right]
            if op == "!=":
                return Interpreter.current_row[left] != Interpreter.current_row[right]
        if isinstance(node.right, AST.STRING) or isinstance(node.right, AST.NUMBER):
            if op == "==":
                return Interpreter.current_row[left] == right
            if op == "!=":
                return Interpreter.current_row[left] != right

    @when(AST.ID)
    def visit(self, node):
        return node.name

    @when(AST.NONE)
    def visit(self, node):
        return None

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
