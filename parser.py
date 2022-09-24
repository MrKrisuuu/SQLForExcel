import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens


def p_error(p):
    if p:
        print(f"Error")


def p_program(p):
    """program : instructions"""
    p[0] = p[1]


def p_instructions_doubler(p):
    """instructions : instruction instructions"""
    p[0] = AST.Instructions(p[1], p[2], p.lineno(1))


def p_instructions(p):
    """instructions : instruction"""
    p[0] = p[1]


def p_instruction_create_table(p):
    """instruction : CREATE TABLE table "(" columns ")" """
    p[0] = AST.Create_Table(p[3], p[5], p.lineno(1))


def p_insert_into(p):
    """instruction : INSERT INTO table "(" columns ")" """
    p[0] = AST.Insert_Into(p[3], p[5], p.lineno(1))


def p_instruction_select_from(p):
    """instruction : SELECT columns FROM table"""
    p[0] = AST.Select_From(p[2], p[4], p.lineno(1))


def p_instruction_select_from_where(p):
    """instruction : SELECT columns FROM table WHERE condition"""
    p[0] = AST.Select_From_Where(p[2], p[4], p[6], p.lineno(1))


def p_columns2(p):
    """columns : column "," columns"""
    p[0] = AST.Columns(p[1], p[3], p.lineno(1))


def p_columns1(p):
    """columns : column"""
    p[0] = p[1]


def p_column(p):
    """column : ID"""
    p[0] = AST.Column(p[1], p.lineno(1))


def p_table(p):
    """table : ID"""
    p[0] = AST.Table(p[1], p.lineno(1))


def p_condition(p):
    """condition : ID EQUAL variable
        | ID NOT_EQUAL variable"""
    p[0] = AST.Condition(AST.ID(p[1], p.lineno(1)), p[2], p[3], p.lineno(1))


def p_variable_string(p):
    """variable : STRING"""
    p[0] = AST.STRING(p[1], p.lineno(1))


def p_variable_number(p):
    """variable : NUMBER"""
    p[0] = AST.NUMBER(p[1], p.lineno(1))


parser = yacc.yacc()