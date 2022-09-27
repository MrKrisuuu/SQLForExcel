import ply.lex as lex
from decimal import Decimal

literals = [",", "(", ")", "=", "*"]

reserved = {
    # create
    "CREATE": "CREATE",
    "TABLE": "TABLE",
    "INSERT": "INSERT",
    "INTO": "INTO",
    # read
    "SELECT": "SELECT",
    "FROM": "FROM",
    "JOIN": "JOIN",
    "ON": "ON",
    "WHERE": "WHERE",
    "GROUP": "GROUP",
    "BY": "BY",
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
    "STRING",
    "NUMBER"
] + list(reserved.values())

t_ignore = " "
t_ignore_COMMENT = "--.*"

t_EQUAL = "=="
t_NOT_EQUAL = "!="


def t_ID(t):
    r"[A-Z]+|([a-z]+)(\.[a-z]+)?"
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
