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
    def __init__(self, table, columns, lineno):
        self.table = table
        self.columns = columns
        super().__init__(lineno)


class Select_From(Node):
    def __init__(self, columns, table, lineno):
        self.columns = columns
        self.table = table
        super().__init__(lineno)


class Select_From_Where(Node):
    def __init__(self, columns, table, condition, lineno):
        self.columns = columns
        self.table = table
        self.condition = condition
        super().__init__(lineno)


class Columns(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Column(Node):
    def __init__(self, name, lineno):
        self.name = name
        super().__init__(lineno)


class Table(Node):
    def __init__(self, name, lineno):
        self.name = name
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


class STRING(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


class NUMBER(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)