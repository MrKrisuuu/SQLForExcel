import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens


def p_error(p):
    if p:
        print(f"Error at line {p.lineno} with {p.value}")


# BASIC STUFF


def p_program(p):
    """program : instructions
        | instruction_select"""
    p[0] = p[1]


def p_instructions_doubler(p):
    """instructions : instruction instructions"""
    p[0] = AST.Instructions(p[1], p[2], p.lineno(1))


def p_instructions(p):
    """instructions : instruction"""
    p[0] = AST.Instructions(p[1], None, p.lineno(1))


# CRUD


def p_create_table(p):
    """instruction : CREATE TABLE table "(" columns ")" """
    p[0] = AST.CreateTable(p[3], p[5], p.lineno(1))


def p_insert_into(p):
    """instruction : INSERT INTO table VALUES values """
    p[0] = AST.InsertInto(p[3], p[5], p.lineno(1))


def p_select(p):
    """instruction_select : SELECT aggregates FROM table joinings whering grouping having ordering"""
    p[0] = AST.SelectFrom(p[2], p[4], p[5], p[6], p[7], p[8], p[9], p.lineno(1))


def p_update(p):
    """instruction : UPDATE table SET sets WHERE condition"""
    p[0] = AST.Update(p[2], p[4], p[6], p.lineno(1))


def p_delete_from(p):
    """instruction : DELETE FROM table WHERE condition"""
    p[0] = AST.DeleteFrom(p[3], p[5], p.lineno(1))


# SELECT


def p_aggregates_doubler(p):
    """aggregates : aggregate "," aggregates
        | column "," aggregates """
    p[0] = AST.Aggregates(p[1], p[3], p.lineno(1))


def p_aggregates(p):
    """aggregates : aggregate
        | column"""
    p[0] = AST.Aggregates(p[1], None, p.lineno(1))


def p_aggregate(p):
    """aggregate : function "(" column ")" """
    p[0] = AST.Aggregate(p[1], p[3], p.lineno(1))


def p_table_shortname(p):
    """table : ID ID"""
    p[0] = AST.Table(AST.ID(p[1], p.lineno(1)), AST.ID(p[2], p.lineno(1)), p.lineno(1))


def p_table(p):
    """table : ID"""
    p[0] = AST.Table(AST.ID(p[1], p.lineno(1)), AST.ID(p[1], p.lineno(1)), p.lineno(1))


def p_joins_on_doubler(p):
    """joinings : joining joinings"""
    p[0] = AST.JoinsOn(p[1], p[2], p.lineno(1))


def p_join_on_nothing(p):
    """joinings : """
    p[0] = AST.NONE()


def p_join_on(p):
    """joining : join_type JOIN table ON condition"""
    p[0] = AST.JoinOn(p[1], p[3], p[5], p.lineno(1))


def p_join_type(p):
    """join_type : LEFT
        | RIGHT
        | FULL"""
    p[0] = AST.ID(p[1], p.lineno(1))


def p_join_type_nothing(p):
    """join_type : """
    p[0] = AST.NONE()


def p_where(p):
    """whering : WHERE condition"""
    p[0] = AST.Where(p[2], p.lineno(1))


def p_where_nothing(p):
    """whering : """
    p[0] = AST.NONE()


def p_group_by(p):
    """grouping : GROUP BY columns"""
    p[0] = AST.GroupBy(p[3], p.lineno(1))


def p_group_by_nothing(p):
    """grouping : """
    p[0] = AST.NONE()


def p_having(p):
    """having : HAVING condition"""
    p[0] = AST.Having(p[2], p.lineno(1))


def p_having_nothing(p):
    """having : """
    p[0] = AST.NONE()


def p_order_by(p):
    """ordering : ORDER BY aggregates"""
    p[0] = AST.OrderBy(p[3], p.lineno(1))


def p_order_by_nothing(p):
    """ordering : """
    p[0] = AST.NONE()


# DOUBLERS

# VALUES
def p_values_doubler(p):
    """values : value "," values"""
    p[0] = AST.Values(p[1], p[3], p.lineno(1))


def p_values(p):
    """values : value"""
    p[0] = AST.Values(p[1], None, p.lineno(1))


def p_value(p):
    """value : "(" variables ")" """
    p[0] = AST.Value(p[2], p.lineno(1))


# VARIABLES
def p_variables_doubler(p):
    """variables : variable "," variables"""
    p[0] = AST.Variables(p[1], p[3], p.lineno(1))


def p_variables(p):
    """variables : variable"""
    p[0] = AST.Variables(p[1], None, p.lineno(1))


def p_variable_string(p):
    """variable : STRING"""
    p[0] = AST.Variable(AST.STRING(p[1], p.lineno(1)), p.lineno(1))


def p_variable_number(p):
    """variable : NUMBER"""
    p[0] = AST.Variable(AST.NUMBER(p[1], p.lineno(1)), p.lineno(1))


# SETS
def p_sets_doubler(p):
    """sets : set "," sets"""
    p[0] = AST.Sets(p[1], p[3], p.lineno(1))


def p_sets(p):
    """sets : set"""
    p[0] = AST.Sets(p[1], None, p.lineno(1))


def p_set(p):
    """set : column "=" variable"""
    p[0] = AST.Set(p[1], p[3], p.lineno(1))


# COLUMNS
def p_columns_doubler(p):
    """columns : column "," columns"""
    p[0] = AST.Columns(p[1], p[3], p.lineno(1))


def p_columns(p):
    """columns : column"""
    p[0] = AST.Columns(p[1], None, p.lineno(1))


def p_column_all(p):
    """column : "*" """
    p[0] = AST.Column(AST.ID(p[1], p.lineno(1)), p.lineno(1))


def p_column_id(p):
    """column : ID"""
    p[0] = AST.Column(AST.ID(p[1], p.lineno(1)), p.lineno(1))


# OTHERS


def p_condition(p):
    """condition : side EQUAL side
        | side NOT_EQUAL side
        | side LESS side
        | side MORE side
        | side LESS_EQUAL side
        | side MORE_EQUAL side"""
    p[0] = AST.Condition(p[1], p[2], p[3], p.lineno(1))


def p_side_variable(p):
    """side : variable"""
    p[0] = AST.Side(p[1], "variable", p.lineno(1))


def p_side_ID(p):
    """side : ID"""
    p[0] = AST.Side(AST.ID(p[1], p.lineno(1)), "column", p.lineno(1))


def p_side_agregate(p):
    """side : aggregate"""
    p[0] = AST.Side(p[1], "aggregate", p.lineno(1))


def p_function(p):
    """function : SUM
        | COUNT
        | AVG
        | MIN
        | MAX"""
    p[0] = AST.ID(p[1], p.lineno(1))


parser = yacc.yacc()