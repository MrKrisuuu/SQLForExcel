class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def accept(self, visitor):
        visitor.visit(self)


class Instructions(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Create_Table(Node):
    def __init__(self, table, columns, lineno):
        self.table = table
        self.columns = columns
        super().__init__(lineno)


class Insert_Into(Node):
    def __init__(self, table, variables, lineno):
        self.table = table
        self.variables = variables
        super().__init__(lineno)


class Select_From(Node):
    def __init__(self, columns, table, joining, whering, grouping, having, ordering, lineno):
        self.columns = columns
        self.table = table
        self.joining = joining
        self.whering = whering
        self.grouping = grouping
        self.having = having
        self.ordering = ordering
        super().__init__(lineno)


class Join_On(Node):
    def __init__(self, table, condition, lineno):
        self.table = table
        self.condition = condition
        super().__init__(lineno)


class Where(Node):
    def __init__(self, condition, lineno):
        self.condition = condition
        super().__init__(lineno)


class Group_By(Node):
    def __init__(self, columns, lineno):
        self.columns = columns
        super().__init__(lineno)


class Having(Node):
    def __init__(self, condition, lineno):
        self.condition = condition
        super().__init__(lineno)


class Order_By(Node):
    def __init__(self, columns, lineno):
        self.columns = columns
        super().__init__(lineno)


class Update(Node):
    def __init__(self, table, sets, condition, lineno):
        self.table = table
        self.sets = sets
        self.condition = condition
        super().__init__(lineno)


class Delete_From(Node):
    def __init__(self, table, condition, lineno):
        self.table = table
        self.condition = condition
        super().__init__(lineno)


class Sets(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Set(Node):
    def __init__(self, column, variable, lineno):
        self.column = column
        self.variable = variable
        super().__init__(lineno)


class Table(Node):
    def __init__(self, full, short, lineno):
        self.full = full
        self.short = short
        super().__init__(lineno)


class Columns(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Condition(Node):
    def __init__(self, left, op, right, lineno):
        self.left = left
        self.op = op
        self.right = right
        super().__init__(lineno)


class ID(Node):
    def __init__(self, name, lineno):
        self.name = name
        super().__init__(lineno)


class NONE(Node):
    def __init__(self, ):
        pass


class Variables(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class STRING(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


class NUMBER(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)