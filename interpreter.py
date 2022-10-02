import AST
from visit import *
import openpyxl

database_name = "database.xlsx"


def insert_first_row(sheet, row, rownum):
    sheet.cell(row=rownum, column= 1).value = "id"
    for i in range(len(row)):
        sheet.cell(row=rownum, column=i+2).value = row[i]


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
    for colnum, column in enumerate(list(columns.keys())):
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

    @when(AST.Create_Database)
    def visit(self, node):
        database = openpyxl.Workbook()
        sheet = database.get_sheet_by_name("Sheet")
        sheet.title = "Basic stuff"
        database.save(database_name)

    @when(AST.Create_Table)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        columns = self.visit(node.columns)

        database = openpyxl.load_workbook(database_name)
        if fullname in database.get_sheet_names():
            table = database.get_sheet_by_name(fullname)
            database.remove_sheet(table)
        table = database.create_sheet(fullname)
        insert_first_row(table, columns, 1)

        database.save(database_name)

    @when(AST.Insert_Into)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        values = self.visit(node.variables)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(fullname)
        for value in values:
            insert_row(table, value, table.max_row+1)
        database.save(database_name)

    @when(AST.Select_From)
    def visit(self, node):
        # SELECT
        columns_select = self.visit(node.columns)

        # FROM
        (fullname, shortname) = self.visit(node.table)
        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(fullname)

        columns_name = read_first_row(table, shortname)

        res = []
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)
            res.append(modified_row)

        # JOIN ON
        joinings = self.visit(node.joining)
        if joinings is not None:
            for ((fullname, shortname), condition_node) in joinings:
                table = database.get_sheet_by_name(fullname)
                columns_name = read_first_row(table, shortname)
                join = []
                for rownum in range(2, table.max_row + 1):
                    row = read_row(table, rownum)
                    modified_row = modify_row(columns_name, row)
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

        # GROUP BY
        columns = self.visit(node.grouping)
        if columns is not None:
            new_res = {}
            for row in res:
                lis = []
                for column in columns:
                    lis.append(row[column])
                tup = tuple(lis)
                if tup in new_res.keys():
                    tmp = new_res[tup]
                    for column_select in columns_select:
                        if column_select not in columns:
                            (function, col) = column_select
                            if function == "COUNT":
                                tmp[column_select] += 1
                            if function == "SUM":
                                tmp[column_select] += row[col]
                            if function == "MIN":
                                tmp[column_select] = min(tmp[column_select], row[col])
                            if function == "MAX":
                                tmp[column_select] = max(tmp[column_select], row[col])
                    new_res[tup] = tmp
                else:
                    tmp = {}
                    for column_select in columns_select:
                        if column_select not in columns:
                            (function, col) = column_select
                            if function == "COUNT":
                                tmp[column_select] = 1
                            if function == "SUM":
                                tmp[column_select] = row[col]
                            if function == "MIN":
                                tmp[column_select] = row[col]
                            if function == "MAX":
                                tmp[column_select] = row[col]
                    new_res[tup] = tmp
            new_res_2 = []
            for row in new_res.keys():
                new_dict = {}
                for (colnum, column) in enumerate(columns):
                    new_dict[column] = row[colnum]
                new_dict = new_dict | new_res[row]
                new_res_2.append(new_dict)
            res = new_res_2

        # HAVING

        # ORDER BY
        ordering = self.visit(node.ordering)
        if ordering is not None:
            for column in reversed(ordering):
                res.sort(key=lambda x: x[columns_name[column]])

        # RETURN
        for row in res:
            line = []
            for column in columns_select:
                if column == "*":
                    line += list(row.values())
                else:
                    line.append(row[column])
            print(line)

    @when(AST.Joins_On)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Join_On)
    def visit(self, node):
        table = self.visit(node.table)
        return (table, node.condition)

    @when(AST.Where)
    def visit(self, node):
        condition = self.visit(node.condition)
        return condition

    @when(AST.Group_By)
    def visit(self, node):
        columns = self.visit(node.columns)
        return columns

    @when(AST.Order_By)
    def visit(self, node):
        columns = self.visit(node.columns)
        return columns

    @when(AST.Update)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        sets = self.visit(node.sets)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(fullname)

        columns_name = read_first_row(table, shortname)
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, rownum)
            modified_row = modify_row(columns_name, row)

            Interpreter.current_row = modified_row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                for (column_name, value) in sets:
                    i = columns_name[column_name]
                    table.cell(row=rownum, column=i + 1).value = value

        database.save(database_name)

    @when(AST.Delete_From)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)

        database = openpyxl.load_workbook(database_name)
        table = database.get_sheet_by_name(fullname)

        columns_name = read_first_row(table, shortname)
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

    @when(AST.Values)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return [left] + right

    @when(AST.Value)
    def visit(self, node):
        value = self.visit(node.value)
        return value

    @when(AST.Variables)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Variable)
    def visit(self, node):
        variable = self.visit(node.variable)
        return variable

    @when(AST.Sets)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Set)
    def visit(self, node):
        column = self.visit(node.column)
        variable = self.visit(node.variable)
        return (column, variable)

    @when(AST.Table)
    def visit(self, node):
        full = self.visit(node.full)
        short = self.visit(node.short)
        return (full, short)

    @when(AST.Aggregates)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Aggregate)
    def visit(self, node):
        function = self.visit(node.function)
        column = self.visit(node.column)
        return (function, column)

    @when(AST.Columns)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Column)
    def visit(self, node):
        column = self.visit(node.column)
        return column

    @when(AST.Condition)
    def visit(self, node):
        (left, left_type) = self.visit(node.left)
        op = node.op
        (right, right_type) = self.visit(node.right)

        left_value = None
        right_value = None

        if left_type == "variable":
            left_value = left
        elif left_type == "column":
            left_value = Interpreter.current_row[left]
        else:
            raise Exception(f"Wrong type: {left_type}")

        if right_type == "variable":
            right_value = right
        elif right_type == "column":
            right_value = Interpreter.current_row[right]
        else:
            raise Exception(f"Wrong type: {right_type}")

        if op == "==":
            return left_value == right_value
        if op == "!=":
            return left_value != right_value
        else:
            raise Exception(f"Wrong operator: {op}")

    @when(AST.Side)
    def visit(self, node):
        side = self.visit(node.side)
        return (side, node.type)

    @when(AST.NONE)
    def visit(self, node):
        return None

    @when(AST.ID)
    def visit(self, node):
        return node.name

    @when(AST.STRING)
    def visit(self, node):
        return str(node.value)

    @when(AST.NUMBER)
    def visit(self, node):
        return float(node.value)
