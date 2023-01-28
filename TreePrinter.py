import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception(f"printTree not defined in class {self.__class__.__name__}")

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.CreateTable)
    def printTree(self, indent=0):
        print("| " * indent + "CREATE TABLE")
        self.table.printTree(indent + 1)
        self.columns.printTree(indent + 2)

    @addToClass(AST.InsertInto)
    def printTree(self, indent=0):
        print("| " * indent + "INSERT INTO")
        self.table.printTree(indent + 1)
        self.variables.printTree(indent + 2)

    @addToClass(AST.SelectFrom)
    def printTree(self, indent=0):
        print("| " * indent + "SELECT")
        self.columns.printTree(indent+1)
        print("| " * indent + "FROM")
        self.table.printTree(indent + 1)
        if self.joining is not None:
            self.joining.printTree(indent)
        if self.whering is not None:
            self.whering.printTree(indent)
        if self.grouping is not None:
            self.grouping.printTree(indent)
        if self.having is not None:
            self.having.printTree(indent)
        if self.ordering is not None:
            self.ordering.printTree(indent)

    @addToClass(AST.JoinsOn)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.JoinOn)
    def printTree(self, indent=0):
        print("| " * indent + "JOIN")
        self.table.printTree(indent + 1)
        print("| " * (indent + 1) + "ON")
        self.condition.printTree(indent + 2)

    @addToClass(AST.Where)
    def printTree(self, indent=0):
        print("| " * indent + "WHERE")
        self.condition.printTree(indent + 1)

    @addToClass(AST.GroupBy)
    def printTree(self, indent=0):
        print("| " * indent + "GROUP BY")
        self.columns.printTree(indent + 1)

    @addToClass(AST.Having)
    def printTree(self, indent=0):
        print("| " * indent + "HAVING")
        self.condition.printTree(indent + 1)

    @addToClass(AST.OrderBy)
    def printTree(self, indent=0):
        print("| " * indent + "ORDER BY")
        self.columns.printTree(indent + 1)

    @addToClass(AST.Update)
    def printTree(self, indent=0):
        print("| " * indent + "UPDATE")
        self.table.printTree(indent + 1)
        print("| " * indent + "SET")
        self.sets.printTree(indent + 1)
        print("| " * indent + "WHERE")
        self.condition.printTree(indent + 1)

    @addToClass(AST.DeleteFrom)
    def printTree(self, indent=0):
        print("| " * indent + "DELETE FROM")
        self.table.printTree(indent + 1)
        print("| " * indent + "WHERE")
        self.condition.printTree(indent + 1)

    @addToClass(AST.Values)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        print("| " * indent + "-----")
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.Value)
    def printTree(self, indent=0):
        self.value.printTree(indent)

    @addToClass(AST.Variables)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        self.variable.printTree(indent)

    @addToClass(AST.Sets)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.Set)
    def printTree(self, indent=0):
        print("| " * indent + "=")
        self.column.printTree(indent + 1)
        self.variable.printTree(indent + 1)

    @addToClass(AST.Table)
    def printTree(self, indent=0):
        self.full.printTree(indent)
        self.short.printTree(indent)

    @addToClass(AST.Aggregates)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.Aggregate)
    def printTree(self, indent=0):
        self.function.printTree(indent)
        self.column.printTree(indent + 1)

    @addToClass(AST.Columns)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        if self.right is not None:
            self.right.printTree(indent)

    @addToClass(AST.Column)
    def printTree(self, indent=0):
        self.column.printTree(indent)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Side)
    def printTree(self, indent=0):
        self.side.printTree(indent)
        print("| " * (indent + 1) + self.type)

    @addToClass(AST.NONE)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.STRING)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.NUMBER)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

