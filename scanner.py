import ply.lex as lex

literals = [",", "(", ")", "=", "*"]

reserved = {
    # create
    "CREATE": "CREATE",
    "TABLE": "TABLE",
    "INSERT": "INSERT",
    "INTO": "INTO",
    "VALUES": "VALUES",
    # read
    "SELECT": "SELECT",
    "FROM": "FROM",
    "LEFT": "LEFT",
    "RIGHT": "RIGHT",
    "FULL": "FULL",
    "JOIN": "JOIN",
    "ON": "ON",
    "WHERE": "WHERE",
    "GROUP": "GROUP",
    "BY": "BY",
    "SUM": "SUM",
    "COUNT": "COUNT",
    "AVG": "AVG",
    "MIN": "MIN",
    "MAX": "MAX",
    "HAVING": "HAVING",
    "ORDER": "ORDER",
    # update
    "UPDATE": "UPDATE",
    "SET": "SET",
    # delete
    "DELETE": "DELETE"
}

tokens = [
    "ID",
    "EQUAL",
    "NOT_EQUAL",
    "LESS",
    "MORE",
    "LESS_EQUAL",
    "MORE_EQUAL",
    "STRING",
    "NUMBER"
] + list(reserved.values())

t_ignore = " "
t_ignore_COMMENT = "--.*"

t_EQUAL = "=="
t_NOT_EQUAL = "!="
t_LESS = "<"
t_MORE = ">"
t_LESS_EQUAL = "<="
t_MORE_EQUAL = ">="


def t_ID(t):
    r"[A-Z]+|([a-z_]+)(\.[a-z_]+)?"
    t.type = reserved.get(t.value, "ID")
    return t


def t_STRING(t):
    r"\"[a-zA-Z]+\""
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r"([0-9]+)(\.[0-9]+)?"
    t.value = float(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Error at line {t.lineno} with {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
