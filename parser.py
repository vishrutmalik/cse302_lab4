from os import scandir
import ply.yacc as yacc
import bxast as bxast
import sys
from scanner import tokens

# Program

def p_program(p):
    """program : declstar"""
    p[0] = bxast.GlobalScope(p[1])

## decl
def p_declstar(p):
    """declstar : declstar decl
                   | """
    if len(p) == 1:
            p[0] = []
    else:
            p[0] = p[1]
            p[0].append(p[2])

def p_decl(p):
    """decl : vardecl
                | procdecl """
    p[0] = p[1]

def p_vardecl(p):
    """vardecl : VAR varinits COLON type SEMICOLON"""
    p[0] = bxast.Vardecl(bxast.Variable(p[2], [p.lineno(1)]), p[6], p[4], [p.lineno(1)])

def p_varinits(p):
    """varinits : IDENT EQ expr varstar"""
    p[0]=bxast.Variables(p[1],p[3],p[4])

def p_varstar(p):
    """varstar : varstar newvar
                    | """
    if len(p) == 1:
            p[0] = []
    else:
            p[0] = p[1]
            p[0].append(p[2])

def p_newvar(p):
    """newvar : COMMA IDENT EQ expr"""
    p[0]=bxast.NewVar(p[2],p[4])

def p_procdecl(p):
    """procdecl : DEF IDENT LPAREN paramsq RPAREN tydeclq block"""
    p[0] = bxast.Procdecl(p[1], p[3], p[7])

def p_paramsq(p):
    """paramsq : params 
                |"""
    if len(p)==0:
        p[0]=[]
    else:
        p[0]=p[1]

def p_params(p):
    """params : param paramstar"""
    p[0]=bxast.Args(p[1],p[2])

def p_paramstar(p):
    """paramstar : paramstar params2
                    | """
    if len(p) == 1:
            p[0] = []
    else:
            p[0] = p[1]
            p[0].append(p[2])

def p_params2(p):
    """params2 : COMMA param"""
    p[0]=p[1]

def p_param(p):
    """param : IDENT morestar COLON type"""
    p[0]=bxast.Param(p[1],p[2],p[4])

def p_morestar(p):
    """morestar : morestar newparam
                    | """
    if len(p) == 1:
            p[0] = []
    else:
            p[0] = p[1]
            p[0].append(p[2])

def p_newparam(p):
    """newparam : COMMA IDENT"""
    p[0]=bxast.newParam(p[1])


def p_eval(p):
    """eval : expr SEMICOLON"""

def p_tydeclq(p):
    """tydeclq : tydecl
                |"""
    if len(p)==0:
        p[0]=[]
    else:
        p[0]=p[1]

def p_tydecl(p):
    """tydecl : COLON type"""
    p[0]=p[1]

# Statements
def p_statement(p):
    """stmt : vardecl
            | assign
            | print
            | ifelse
            | while
            | block
            | jump """
    p[0] = p[1]

def p_statements(p):
    """stmts :
             | stmts stmt"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])



## Assign

def p_assign(p):
    """assign : IDENT EQ expr SEMICOLON"""
    p[0] = bxast.Assign(bxast.Variable(p[1], [p.lineno(1)]), p[3], [p.lineno(2)])

## Print

def p_print(p):
    """print : PRINT LPAREN expr RPAREN SEMICOLON"""
    p[0] = bxast.Print(p[3], [p.lineno(1)])

## Return

def p_return(p):
    """return : RETURN exprq SEMICOLON"""
    p[0] = p[2]

def p_exprq(p):
    """exprq : expr 
                |"""
    if len(p)==0:
        p[0]=[]
    else:
        p[0]=p[1]

## Ifelse

def p_ifelse(p):
    """ifelse : IF LPAREN expr RPAREN block ifrest"""
    p[0] = bxast.Ifelse(p[3], p[5], p[6], [p.lineno(1)])

## Ifrest

def p_ifrest(p):
    """ifrest :
                | ELSE block
                | ELSE ifelse"""
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = p[2]

## While

def p_while(p):
    """ while : WHILE LPAREN expr RPAREN block"""
    p[0] = bxast.While(p[3], p[5], [p.lineno(1)])

## Jump 

def p_jump(p):
    """ jump : BREAK SEMICOLON
              | CONTINUE SEMICOLON"""
    p[0] = bxast.Jump(p[1], [p.lineno(1)])

## Block

def p_block(p):
    """block : LBRACE stmts RBRACE"""
    p[0] = bxast.Block(p[2])

# Expressions

## Variables

def p_expr_ident(p):
    """expr : IDENT"""
    p[0] = bxast.Variable(p[1], [p.lineno(1)])

## Numbers

def p_expr_number(p):
    """expr : NUMBER"""
    p[0] = bxast.Number(p[1], [p.lineno(1)])

## Booleans

def p_expr_bool(p):
    """expr : TRUE
            | FALSE """
    p[0] = bxast.Bool(p[1], [p.lineno(1)])

## Types

def p_types(p):
    """ type : INT
              | BOOL"""
    p[0] = p[1]

## Parentheses

def p_expr_parens(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]

## Binary Operators

def p_expr_plus(p):
    """expr : expr PLUS expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('PLUS', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_minus(p):
    """expr : expr MINUS expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('MINUS', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_times(p):
    """expr : expr TIMES expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('TIMES', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_div(p):
    """expr : expr DIV expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('DIV', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_modulus(p):
    """expr : expr MODULUS expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('MODULUS', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_bitand(p):
    """expr : expr BITAND expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BITAND', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_bitor(p):
    """expr : expr BITOR expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BITOR', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_bitxor(p):
    """expr : expr BITXOR expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BITXOR', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_bitshl(p):
    """expr : expr SHL expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BITSHL', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_bitshr(p):
    """expr : expr SHR expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BITSHR', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_lt(p):
    """expr : expr LT expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('LT', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_gt(p):
    """expr : expr GT expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('GT', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_lte(p):
    """expr : expr LTE expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('LTE', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_gte(p):
    """expr : expr GTE expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('GTE', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_equals(p):
    """expr : expr BOOLEQ expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('EQUALS', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_nequals(p):
    """expr : expr NEQUALS expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('NEQUALS', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_booland(p):
    """expr : expr BOOLAND expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BOOLAND', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

def p_expr_boolor(p):
    """expr : expr BOOLOR expr"""
    p[0] = bxast.BinopApp(bxast.BinOp('BOOLOR', [p.lineno(2)]), p[1], p[3], [p.lineno(2)])

## Procedure Calls

def p_expr_procedure(p):
    """expr : IDENT LPAREN exprsq RPAREN"""
    p[0] = bxast.ExprProcedureCall(p[1],p[3])


def p_exprsq(p):
    """exprsq : exprs 
                |"""
    if len(p)==0:
        p[0]=[]
    else:
        p[0]=p[1]

def p_exprs(p):
    """exprs : expr exprstar"""
    p[0]=bxast.Args(p[1],p[2])

def p_exprstar(p):
    """exprstar : exprstar exprs2
                    | """
    if len(p) == 1:
            p[0] = []
    else:
            p[0] = p[1]
            p[0].append(p[2])

def p_exprs2(p):
    """exprs2 : COMMA expr"""
    p[0]=p[1]


## Unary Operators

def p_expr_uminus(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = bxast.UnopApp(bxast.UnOp('UMINUS', [p.lineno(1)]), p[2], [p.lineno(1)])

def p_expr_bitcompl(p):
    """expr : BITCOMPL expr"""
    p[0] = bxast.UnopApp(bxast.UnOp('BITCOMPL', [p.lineno(1)]), p[2], [p.lineno(1)])

def p_expr_boolnot(p):
    """expr : BOOLNOT expr"""
    p[0] = bxast.UnopApp(bxast.UnOp('BOOLNOT', [p.lineno(1)]), p[2], [p.lineno(1)])

def p_error(p):
    if p:
        print(f"Syntax error on line {p.lineno}")
        sys.exit(1)
    else:
         print("Syntax error at EOF")
         sys.exit(1)

precedence = (
    ('left', 'BOOLOR'),
    ('left', 'BOOLAND'),
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('nonassoc', 'BOOLEQ', 'NEQUALS'),
    ('nonassoc', 'LT', 'GT', 'LTE', 'GTE'),
    ('left', 'SHL', 'SHR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'MODULUS'),
    ('right', 'BOOLNOT', 'UMINUS'),
    ('right', 'BITCOMPL')
)

parser = yacc.yacc(start='program')
