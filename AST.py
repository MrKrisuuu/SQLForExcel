class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def accept(self, visitor):
        return visitor.visit(self)


# BASIC STUFF


class Instructions(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


# CRUD


class CreateTable(Node):
    def __init__(self, table, columns, lineno):
        self.table = table
        self.columns = columns
        super().__init__(lineno)


class InsertInto(Node):
    def __init__(self, table, variables, lineno):
        self.table = table
        self.variables = variables
        super().__init__(lineno)


class SelectFrom(Node):
    def __init__(self, columns, table, joining, whering, grouping, having, ordering, lineno):
        self.columns = columns
        self.table = table
        self.joining = joining
        self.whering = whering
        self.grouping = grouping
        self.having = having
        self.ordering = ordering
        super().__init__(lineno)


class Update(Node):
    def __init__(self, table, sets, condition, lineno):
        self.table = table
        self.sets = sets
        self.condition = condition
        super().__init__(lineno)


class DeleteFrom(Node):
    def __init__(self, table, condition, lineno):
        self.table = table
        self.condition = condition
        super().__init__(lineno)


# SELECT


class Aggregates(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Aggregate(Node):
    def __init__(self, function, column, lineno):
        self.function = function
        self.column = column
        super().__init__(lineno)


class Table(Node):
    def __init__(self, fullname, shortname, lineno):
        self.fullname = fullname
        self.shortname = shortname
        super().__init__(lineno)


class JoinsOn(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class JoinOn(Node):
    def __init__(self, join_type, table, condition, lineno):
        self.join_type = join_type
        self.table = table
        self.condition = condition
        super().__init__(lineno)


class Where(Node):
    def __init__(self, condition, lineno):
        self.condition = condition
        super().__init__(lineno)


class GroupBy(Node):
    def __init__(self, columns, lineno):
        self.columns = columns
        super().__init__(lineno)


class Having(Node):
    def __init__(self, condition, lineno):
        self.condition = condition
        super().__init__(lineno)


class OrderBy(Node):
    def __init__(self, columns, lineno):
        self.columns = columns
        super().__init__(lineno)


# DOUBLERS

# VALUES
class Values(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Value(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


# VARIABLES
class Variables(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Variable(Node):
    def __init__(self, variable, lineno):
        self.variable = variable
        super().__init__(lineno)


# SETS
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


# COLUMNS
class Columns(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class Column(Node):
    def __init__(self, column, lineno):
        self.column = column
        super().__init__(lineno)


# OTHERS


class Condition(Node):
    def __init__(self, left, op, right, lineno):
        self.left = left
        self.op = op
        self.right = right
        super().__init__(lineno)


class Side(Node):
    def __init__(self, side, type, lineno):
        self.side = side
        self.type = type
        super().__init__(lineno)


class NONE(Node):
    def __init__(self):
        pass


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