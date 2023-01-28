import AST
from visit import *
import openpyxl

ROW_COLUMN_NAMES = 1


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


def get_columns_names(sheet, shortname):  # {column_name -> id_column}
    row = sheet[ROW_COLUMN_NAMES]
    data = {}
    for (i, cell) in enumerate(row):
        data[shortname + "." + cell.value] = i
    return data


def read_row(sheet, column_names, rownum):  # {column_name -> value}
    row = sheet[rownum]
    modified_row = {}
    for column_name in column_names.keys():
        modified_row[column_name] = row[column_names[column_name]].value
    return modified_row


class Interpreter(object):
    current_row = None

    def __init__(self, name):
        self.name = name

    # BASIC STUFF

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

    # CRUD

    @when(AST.CreateTable)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        columns = self.visit(node.columns)
        database = openpyxl.load_workbook(self.name)
        if fullname in database.get_sheet_names():
            table = database.get_sheet_by_name(fullname)
            database.remove_sheet(table)
        table = database.create_sheet(fullname)
        insert_first_row(table, columns, 1)
        database.save(self.name)

    @when(AST.InsertInto)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        values = self.visit(node.variables)
        database = openpyxl.load_workbook(self.name)
        table = database.get_sheet_by_name(fullname)
        for value in values:
            insert_row(table, value, table.max_row + 1)
        database.save(self.name)

    @when(AST.SelectFrom)
    def visit(self, node):
        # SELECT
        columns_select = self.visit(node.columns)  # [column_name]

        # FROM
        (fullname, shortname) = self.visit(node.table)
        database = openpyxl.load_workbook(self.name)
        table = database.get_sheet_by_name(fullname)

        column_names = get_columns_names(table, shortname)

        res = []
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, column_names, rownum)
            res.append(row)

        # JOIN ON
        left = res
        joinings = self.visit(node.joining)
        if joinings is not None:
            for (join_type, (fullname, shortname), condition_node) in joinings:
                table = database.get_sheet_by_name(fullname)
                column_names = get_columns_names(table, shortname)
                right = []
                for rownum in range(2, table.max_row + 1):
                    row = read_row(table, column_names, rownum)
                    right.append(row)
                new_res = []
                if join_type is None:
                    for left_row in left:
                        for right_row in right:
                            joined_row = left_row | right_row
                            Interpreter.current_row = joined_row
                            condition = self.visit(condition_node)
                            Interpreter.current_row = None
                            if condition:
                                new_res.append(joined_row)
                    left = new_res
                if join_type == "LEFT":
                    for left_row in left:
                        added = 0
                        for right_row in right:
                            joined_row = left_row | right_row
                            Interpreter.current_row = joined_row
                            condition = self.visit(condition_node)
                            Interpreter.current_row = None
                            if condition:
                                added = 1
                                new_res.append(joined_row)
                        if added == 0:
                            joined_row = left_row | dict.fromkeys(right[0], None)
                            new_res.append(joined_row)

                    left = new_res
                if join_type == "RIGHT":
                    raise Exception("RIGHT is not implemented.")
                if join_type == "FULL":
                    raise Exception("FULL is not implemented.")
        res = left

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
                            if col == "*" or row[col] is not None:
                                if function == "COUNT":
                                    tmp[column_select] += 1
                                if function == "SUM":
                                    tmp[column_select] += row[col]
                                if function == "AVG":
                                    tmp[column_select] = (tmp[column_select][0] + row[col], tmp[column_select][1] + 1)
                                if function == "MIN":
                                    if tmp[column_select] is None:
                                        tmp[column_select] = row[col]
                                    else:
                                        tmp[column_select] = min(tmp[column_select], row[col])
                                if function == "MAX":
                                    if tmp[column_select] is None:
                                        tmp[column_select] = row[col]
                                    else:
                                        tmp[column_select] = max(tmp[column_select], row[col])
                else:
                    tmp = {}
                    for column_select in columns_select:
                        if column_select not in columns:
                            (function, col) = column_select
                            if col == "*" or row[col] is not None:
                                if function == "COUNT":
                                    tmp[column_select] = 1
                                if function == "SUM":
                                    tmp[column_select] = row[col]
                                if function == "AVG":
                                    tmp[column_select] = (row[col], 1)
                                if function == "MIN":
                                    tmp[column_select] = row[col]
                                if function == "MAX":
                                    tmp[column_select] = row[col]
                            else:
                                if function == "COUNT":
                                    tmp[column_select] = 0
                                if function == "SUM":
                                    tmp[column_select] = 0
                                if function == "AVG":
                                    tmp[column_select] = (0, 0)
                                if function == "MIN":
                                    tmp[column_select] = None
                                if function == "MAX":
                                    tmp[column_select] = None
                    new_res[tup] = tmp
            for tup in new_res.keys():
                tmp = new_res[tup]
                for column_select in columns_select:
                    if column_select not in columns:
                        (function, col) = column_select
                        if function == "AVG":
                            if tmp[column_select][1] == 0:
                                tmp[column_select] = None
                            else:
                                tmp[column_select] = tmp[column_select][0] / tmp[column_select][1]
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
        new_res = []
        for row in res:
            Interpreter.current_row = row
            condition = self.visit(node.having)
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
        print(columns_select)
        for row in res:
            line = []
            for column in columns_select:
                if column == "*":
                    line += list(row.values())
                else:
                    line.append(row[column])
            print(line)
        print()

    @when(AST.Update)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        sets = self.visit(node.sets)
        database = openpyxl.load_workbook(self.name)
        table = database.get_sheet_by_name(fullname)
        column_names = get_columns_names(table, shortname)
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, column_names, rownum)
            Interpreter.current_row = row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                for (column_name, value) in sets:
                    i = column_names[column_name]
                    table.cell(row=rownum, column=i + 1).value = value
        database.save(self.name)

    @when(AST.DeleteFrom)
    def visit(self, node):
        (fullname, shortname) = self.visit(node.table)
        database = openpyxl.load_workbook(self.name)
        table = database.get_sheet_by_name(fullname)
        column_names = get_columns_names(table, shortname)
        dels = 0
        for rownum in range(2, table.max_row + 1):
            row = read_row(table, column_names, rownum - dels)
            Interpreter.current_row = row
            condition = self.visit(node.condition)
            Interpreter.current_row = None
            if condition:
                table.delete_rows(rownum - dels, 1)
                dels += 1
        database.save(self.name)

    # SELECT

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

    @when(AST.Table)
    def visit(self, node):
        full = self.visit(node.full)
        short = self.visit(node.short)
        return (full, short)

    @when(AST.JoinsOn)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.JoinOn)
    def visit(self, node):
        join_type = self.visit(node.join_type)
        table = self.visit(node.table)
        return (join_type, table, node.condition)

    @when(AST.Where)
    def visit(self, node):
        condition = self.visit(node.condition)
        return condition

    @when(AST.GroupBy)
    def visit(self, node):
        columns = self.visit(node.columns)
        return columns

    @when(AST.Having)
    def visit(self, node):
        condition = self.visit(node.condition)
        return condition

    @when(AST.OrderBy)
    def visit(self, node):
        columns = self.visit(node.columns)
        return columns

    # DOUBLERS

    # VALUES
    @when(AST.Values)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if right is None:
            return [left]
        return [left] + right

    @when(AST.Value)
    def visit(self, node):
        value = self.visit(node.value)
        return value

    # VARIABLES
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

    # SETS
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

    # COLUMNS
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

    # OTHERS

    @when(AST.Condition)
    def visit(self, node):
        (left, left_type) = self.visit(node.left)
        op = node.op
        (right, right_type) = self.visit(node.right)

        if left is None or right is None:
            return False

        left_value = None
        right_value = None

        if left_type == "variable":
            left_value = left
        elif left_type == "column":
            left_value = Interpreter.current_row[left]
        elif left_type == "aggregate":
            left_value = Interpreter.current_row[left]
        else:
            raise Exception(f"Wrong type: {left_type}")

        if right_type == "variable":
            right_value = right
        elif right_type == "column":
            right_value = Interpreter.current_row[right]
        elif right_type == "aggregate":
            right_value = Interpreter.current_row[right]
        else:
            raise Exception(f"Wrong type: {right_type}")

        if op == "==":
            return left_value == right_value
        if op == "!=":
            return left_value != right_value
        if op == "<":
            return left_value < right_value
        if op == ">":
            return left_value > right_value
        if op == "<=":
            return left_value <= right_value
        if op == ">=":
            return left_value >= right_value
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
