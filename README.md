# COMP3173 Compiler Project - Mathematical Expression Analyzer

## Project Overview

This project involves developing a small analyzer for mathematical expressions. The language is simplified and consists of:
- Numbers and boolean values
- Numeric operators (+, *)
- Relational operators (<, =)
- Variable declarations
- Function declarations
- Function applications

## Project Structure

The project is organized into **4 levels** of increasing complexity that must be completed in sequence.

### Level 1: Basic Arithmetic
- Grammar: `level1_grammar.txt`
- Parsing Table: `level1_parsing_table.csv`
- Type Rules: `level1_type_rule.txt`
- Features: Basic arithmetic expressions with numbers and booleans

### Level 2: Conditionals
- Grammar: `level2_grammar.txt`
- Parsing Table: `level2_parsing_table.csv`
- Features: Adds if-then-else expressions and relational operators

### Level 3: Variables
- Grammar: `level3_grammar.txt`
- Parsing Table: `level3_parsing_table.csv`
- Features: Adds variable declarations and references

### Level 4: Functions
- Grammar: `level4_grammar.txt`
- Parsing Table: `level4_parsing_table.csv`
- Features: Adds function declarations and function applications

## Implementation Options

Students can choose to implement the project in one of three languages:

### C Language
- **Difficulty**: Most difficult
- **Files**: `main.c`, `lexer.c/.h`, `parser.c/.h`, `type_checker.c/.h`, `ast_gen.c/.h`, `symbol_table.c/.h`, `lib.c/.h`
- **Build**: Use `make.bat` or compile manually with `gcc`
- **Note**: Limited standard library support; students must implement everything themselves

### Java
- **Difficulty**: Moderate
- **Files**: `Main.java`, `Lexer.java`
- **Build**: `javac *.java`
- **Run**: `java Main <test_file>`
- **Note**: Better error handling than C

### Python
- **Difficulty**: Easiest
- **Files**: `main.py`, `lexer.py`
- **Run**: `python main.py <test_file>`
- **Note**: Can use `csv`, `json`, and `re` packages from standard library

## Components to Implement

1. **Lexer**: Tokenizes the input source code
   - Output: `<filename>_lexer.json`

2. **Parser**: Builds parse tree from tokens
   - Output: `<filename>_parse.json`

3. **Type Checker**: Performs semantic analysis and type checking
   - Output: `<filename>_type.json`

4. **AST Generator**: Generates abstract syntax tree
   - Output: `<filename>_ast.json`

5. **Symbol Table**: Manages variable and function declarations

## Test Cases

- **Level 1**: `l1t1`, `l1t2`, `l1t3`, `l1t4`
- **Level 2**: `l2t1`, `l2t2`, `l2t3`, `l2t4`
- **Level 3**: `l3t1`, `l3t2`, `l3t3`, `l3t4`
- **Level 4**: `l4t1`, `l4t2`, `l4t3`, `l4t4`
- **Bonus**: `bpt1`, `brt1`
- **Advanced**: `ultra`

## Sample Implementation

A reference implementation is provided:
- `sample_linux.exe` (Linux)
- `sample_mac.exe` (macOS)
- `sample_windows.exe` (Windows)

Run with: `./sample_linux.exe <test_file>`

The sample will generate JSON output files showing the expected format.

## Building and Running

### C Version
```bash
gcc lexer.c -c
gcc symbol_table.c -c
gcc parser.c -c
gcc type_checker.c -c
gcc ast_gen.c -c
gcc lib.c -c
gcc main.c lexer.o symbol_table.o parser.o type_checker.o ast_gen.o lib.o -o fun.exe
./fun.exe <test_file>
```

### Python Version
```bash
python main.py <test_file>
```

### Java Version
```bash
javac *.java
java Main <test_file>
```

## Important Notes

⚠️ **DO NOT CHANGE FILE NAMES** - The autograder expects specific file names.

⚠️ **NO EXTERNAL LIBRARIES** - Only use the standard library of your chosen language.

## Output Format

All output must be in JSON format:
- Lexer output: Array of tokens with `name` and `lexeme` fields
- Parser output: Parse tree with `name`, `children`, and optional `lexeme` fields
- Type checker output: Parse tree with additional `type` field
- AST output: Simplified abstract syntax tree

## Advanced Features (ultra)

The `ultra` test case demonstrates general-purpose computation including:
- Boolean operations (conjunction, disjunction, negation)
- Arithmetic operations (predecessor, subtraction, negation, division)
- Relational operations (less than, equal, greater than)

These functions are implemented in the language itself, showcasing its computational capabilities.
