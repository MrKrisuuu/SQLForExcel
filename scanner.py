import ply.lex as lex
from decimal import Decimal

literals = [",", "(", ")", "=", "*"]

reserved = {
    "CREATE": "CREATE",
    "TABLE": "TABLE",
    "INSERT": "INSERT",
    "INTO": "INTO",
    "UPDATE": "UPDATE",
    "SET": "SET",
    "DELETE": "DELETE",
    "SELECT": "SELECT",
    "FROM": "FROM",
    "WHERE": "WHERE"
}

tokens = [
    "EQUAL",
    "NOT_EQUAL",
    "ID",
    "STRING",
    "NUMBER"
] + list(reserved.values())

t_ignore = " "
t_ignore_COMMENT = "--.*"

t_EQUAL = "=="
t_NOT_EQUAL = "!="


def t_ID(t):
    r"[a-z]+|[A-Z]+"
    t.type = reserved.get(t.value, "ID")
    return t


def t_STRING(t):
    r"\"[a-zA-Z]+\""
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r"([0-9]+)(.[0-9]+)?"
    t.value = float(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Error at line {t.lineno} with {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
