import argparse
import os

from scanner import lexer
from parser import parser
dirname, filename = os.path.split(os.path.abspath(__file__))

def get_ast(fname):
    with open(f"{dirname}/{fname}", 'r') as f:
            ast = parser.parse(f.read(), lexer=lexer)
            ast.check_syntax()
            lexer.lineno = 1

    return ast

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    args = parser.parse_args()
    
    get_ast(args.fname)
    
