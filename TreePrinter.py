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
        self.right.printTree(indent)

    @addToClass(AST.Create_Table)
    def printTree(self, indent=0):
        print("| " * indent + "CREATE TABLE")
        self.table.printTree(indent + 1)
        self.columns.printTree(indent + 2)

    @addToClass(AST.Insert_Into)
    def printTree(self, indent=0):
        print("| " * indent + "INSERT INTO")
        self.table.printTree(indent + 1)
        self.columns.printTree(indent + 2)

    @addToClass(AST.Select_From)
    def printTree(self, indent=0):
        print("| " * indent + "SELECT")
        self.columns.printTree(indent+1)
        print("| " * indent + "FROM")
        self.table.printTree(indent + 1)

    @addToClass(AST.Select_From_Where)
    def printTree(self, indent=0):
        print("| " * indent + "SELECT")
        self.columns.printTree(indent + 1)
        print("| " * indent + "FROM")
        self.table.printTree(indent + 1)
        print("| " * indent + "WHERE")
        self.condition.printTree(indent + 1)

    @addToClass(AST.Columns)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.Column)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.Table)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.STRING)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.NUMBER)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

