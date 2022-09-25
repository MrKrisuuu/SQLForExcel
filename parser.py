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
    """instruction : INSERT INTO table "(" variables ")" """
    p[0] = AST.Insert_Into(p[3], p[5], p.lineno(1))


def p_update(p):
    """instruction : UPDATE table SET sets WHERE condition"""
    p[0] = AST.Update(p[2], p[4], p[6], p.lineno(1))


def p_delete_from(p):
    """instruction : DELETE FROM table WHERE condition"""
    p[0] = AST.Delete_From(p[3], p[5], p.lineno(1))


def p_instruction_select_from(p):
    """instruction : SELECT columns FROM table"""
    p[0] = AST.Select_From(p[2], p[4], p.lineno(1))


def p_instruction_select_from_where(p):
    """instruction : SELECT columns FROM table WHERE condition"""
    p[0] = AST.Select_From_Where(p[2], p[4], p[6], p.lineno(1))


def p_sets_doubler(p):
    """sets : set "," sets"""
    p[0] = AST.Sets(p[1], p[3], p.lineno(1))


def p_sets(p):
    """sets : set"""
    p[0] = p[1]


def p_set(p):
    """set : column "=" variable"""
    p[0] = AST.Set(p[1], p[3], p.lineno(1))


def p_columns_doubler(p):
    """columns : column "," columns"""
    p[0] = AST.Columns(p[1], p[3], p.lineno(1))


def p_columns(p):
    """columns : column"""
    p[0] = p[1]


def p_column_id(p):
    """column : ID"""
    p[0] = AST.ID(p[1], p.lineno(1))


def p_column_all(p):
    """column : "*" """
    p[0] = AST.ID(p[1], p.lineno(1))


def p_table(p):
    """table : ID"""
    p[0] = AST.ID(p[1], p.lineno(1))


def p_condition(p):
    """condition : ID EQUAL variable
        | ID NOT_EQUAL variable"""
    p[0] = AST.Condition(AST.ID(p[1], p.lineno(1)), p[2], p[3], p.lineno(1))


def p_variables_doubler(p):
    """variables : variable "," variables"""
    p[0] = AST.Variables(p[1], p[3], p.lineno(1))


def p_variables(p):
    """variables : variable"""
    p[0] = p[1]


def p_variable_string(p):
    """variable : STRING"""
    p[0] = AST.STRING(p[1], p.lineno(1))


def p_variable_number(p):
    """variable : NUMBER"""
    p[0] = AST.NUMBER(p[1], p.lineno(1))


parser = yacc.yacc()