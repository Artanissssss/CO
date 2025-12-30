from lexer import Lexer
from parser import Parser
from type_checker import TypeChecker
from ast_gen import ASTGenerator
import sys
import json

# WARNING:
# - You are not allowed to use any external libraries other than the standard library
# - Please do not modify the file name of the entry file 'main.py'
# - Our autograder will test your code by running 'python main.py <test_file>'
#   The current directory will be the same directory as the entry file
#   So please make sure your import statement is correct

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <test_file>")
        sys.exit(1)

    file_name = sys.argv[1]
    
    # Determine level based on filename
    level = 1
    if 'l2' in file_name or 'L2' in file_name:
        level = 2
    elif 'l3' in file_name or 'L3' in file_name:
        level = 3
    elif 'l4' in file_name or 'L4' in file_name:
        level = 4
    elif file_name in ['bpt1', 'brt1', 'ultra']:
        # Bonus tests are Level 4
        level = 4

    with open(file_name, 'r') as f:
        # Read file to string
        source_code = f.read()
        
        # Stage 1: Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Write lexer output
        lexer_output = [token.to_dict() for token in tokens]
        with open(f'{file_name}_lexer.json', 'w') as out:
            json.dump(lexer_output, out, indent=4)
        
        # Stage 2: Parsing
        parser = Parser(tokens, level)
        parse_tree = parser.parse()
        
        # Write parser output
        if parse_tree:
            with open(f'{file_name}_parse.json', 'w') as out:
                json.dump(parse_tree.to_dict(), out, indent=2)
        
        # Stage 3: Type Checking
        type_checker = TypeChecker(parse_tree, level)
        typed_tree = type_checker.check()
        
        # Write type checker output
        if typed_tree:
            with open(f'{file_name}_type.json', 'w') as out:
                json.dump(type_checker.node_to_dict(typed_tree), out, indent=2)
        
        # Stage 4: AST Generation
        ast_gen = ASTGenerator(typed_tree)
        ast = ast_gen.generate()
        
        # Write AST output
        if ast:
            with open(f'{file_name}_ast.json', 'w') as out:
                json.dump([ast.to_dict()], out, indent=4)

