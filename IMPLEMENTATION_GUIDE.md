# Implementation Guide

This guide provides step-by-step instructions for implementing the mathematical expression analyzer.

## Phase 1: Setup and Understanding

### Step 1: Read the Documentation
1. Read `README.md` for project overview
2. Study `LANGUAGE_SPEC.md` for language details
3. Examine the grammar files:
   - `level1_grammar.txt`
   - `level2_grammar.txt`
   - `level3_grammar.txt`
   - `level4_grammar.txt`
4. Review the parsing tables (CSV files)
5. Understand the type rules in `level1_type_rule.txt`

### Step 2: Choose Your Language
- **Python** (recommended for beginners): Easiest, has helpful libraries
- **Java** (moderate difficulty): Good error handling, strong typing
- **C** (advanced): Most challenging, full control

### Step 3: Run the Sample Implementation
```bash
# Linux/macOS: Make the sample executable runnable
chmod +x sample_linux.exe
./sample_linux.exe l1t1

# Windows: Use the Windows executable
sample_windows.exe l1t1

# Examine the generated JSON files (use 'type' instead of 'cat' on Windows)
cat l1t1_lexer.json
cat l1t1_parse.json
cat l1t1_type.json
cat l1t1_ast.json
```

## Phase 2: Implement the Lexer

### Understanding the Lexer
The lexer (lexical analyzer) converts source code text into a sequence of tokens.

**Input**: Raw source code string
**Output**: JSON array of tokens with `name` and `lexeme` fields

### Token Types
You need to recognize:
- Keywords: `Compute`, `Let`, `be`, `if`, `then`, `else`, `maps`, `to`, `num`, `bool`
- Literals: numbers (`num_lit`), booleans (`bool_lit`: `true`, `false`)
- Operators: `+`, `*`, `<`, `=`, `>>`
- Delimiters: `(`, `)`, `,`, `.`
- Identifiers: variable and function names

### Implementation Steps
1. Read the input file
2. Tokenize the input:
   - Skip whitespace
   - Match keywords first (before identifiers)
   - Match numbers: sequence of digits
   - Match identifiers: letter followed by letters/digits
   - Match operators and delimiters
3. Create a token object for each match with:
   - `name`: token type
   - `lexeme`: actual text matched
4. Write output to `<filename>_lexer.json`

### Python Example Structure
```python
class Token:
    def __init__(self, name, lexeme):
        self.name = name
        self.lexeme = lexeme
    
    def to_dict(self):
        return {"name": self.name, "lexeme": self.lexeme}

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.tokens = []
    
    def tokenize(self):
        # Skip whitespace
        # Try to match keywords
        # Try to match numbers
        # Try to match identifiers
        # Try to match operators
        # Return list of tokens
        pass
```

### Test Your Lexer
```bash
# Python
python main.py l1t1
diff l1t1_lexer.json <expected_output>

# C
./fun.exe l1t1

# Java
java Main l1t1
```

## Phase 3: Implement the Parser

### Understanding the Parser
The parser analyzes the token sequence according to grammar rules and builds a parse tree.

**Input**: List of tokens from lexer
**Output**: JSON parse tree

### Parser Algorithm
You must implement an **LR(1) parser** using the provided parsing tables.

#### LR Parsing Overview
1. Use a **stack** to store states
2. Use a **parsing table** with:
   - ACTION table: what to do for each (state, terminal) pair
     - `sN`: Shift and push state N
     - `rN`: Reduce by grammar rule N
     - `acc`: Accept
   - GOTO table: next state after reduction for (state, non-terminal)

#### LR Parsing Algorithm
```
1. Initialize stack with state 0
2. Set input pointer to first token
3. Repeat:
   a. Let s = top state on stack
   b. Let a = current input token
   c. Look up ACTION[s, a]:
      - If "shift n": push token and state n onto stack, advance input
      - If "reduce by rule X -> Y1...Yk":
        * Pop 2k symbols from stack (k symbols and k states)
        * Let s' = new top state
        * Push X and GOTO[s', X] onto stack
        * Build parse tree node for X with Y1...Yk as children
      - If "accept": return parse tree
      - If error: report syntax error
```

### Reading the Parsing Table
The CSV file has:
- First column: State number
- ACTION columns: terminals (tokens)
- GOTO columns: non-terminals

Example:
```
State,+,*,num_lit,...,Z,L,E,A,M,U,P,C
0,,,s9,...,1,2,,,,,,
```
This means: From state 0, on `num_lit`, shift and go to state 9.

### Implementation Steps
1. Load the parsing table from CSV
2. Initialize the stack with state 0
3. For each token from lexer:
   - Look up action in table
   - Execute shift or reduce
   - Build parse tree nodes during reductions
4. Write parse tree to `<filename>_parse.json`

### Parse Tree Structure
```json
{
  "name": "NonTerminal",
  "children": [
    {"name": "Terminal", "lexeme": "value"},
    {"name": "NonTerminal", "children": [...]}
  ]
}
```

## Phase 4: Implement Type Checker

### Understanding Type Checking
The type checker performs semantic analysis, ensuring expressions have valid types.

**Input**: Parse tree from parser
**Output**: Parse tree annotated with type information

### Type Rules
Refer to `level1_type_rule.txt` for examples. You need to:
1. Traverse the parse tree (post-order)
2. Assign types to leaf nodes (literals, identifiers)
3. Propagate types up the tree
4. Check type constraints at each node

### Type Assignment Rules
- `num_lit` → type = `num`
- `bool_lit` → type = `bool`
- `A -> A + M` → type = `num` if both children are `num`, else `TYPE_ERROR`
- `M -> M * U` → type = `num` if both children are `num`, else `TYPE_ERROR`
- `if B then A else A` → type = type of A (both A must have same type, B must be bool)

### Implementation Steps
1. Traverse parse tree recursively
2. For each node:
   - Compute types of children first
   - Apply type rule for this node
   - Assign type to node
3. Handle symbol table for variables and functions (Level 3+)
4. Write annotated tree to `<filename>_type.json`

## Phase 5: Implement Symbol Table (Level 3+)

### Purpose
Track variable and function declarations, their types, and scopes.

### Data Structure
```python
class SymbolTable:
    def __init__(self):
        self.symbols = {}  # name -> {type, value}
    
    def declare(self, name, typ):
        self.symbols[name] = {'type': typ}
    
    def lookup(self, name):
        return self.symbols.get(name)
```

### When to Use
- **Declaration**: When processing `Let T id be E .`
  - Add identifier with its type to symbol table
- **Reference**: When processing identifier in expression
  - Look up identifier in symbol table
  - Use its type for type checking

## Phase 6: Implement AST Generator

### Understanding AST
The Abstract Syntax Tree is a simplified version of the parse tree, removing unnecessary syntax elements.

**Input**: Typed parse tree
**Output**: Simplified AST in JSON

### AST Structure
Remove intermediate non-terminals and keep only:
- Compute statements
- Expressions (operators with operands)
- Literals
- Variables
- Function definitions and applications

### Transformation Examples

Parse tree:
```
C -> Compute E .
  E -> A
    A -> M
      M -> U
        U -> P
          P -> num_lit "1"
```

AST:
```json
{
  "name": "Compute",
  "children": [
    {"name": "1"}
  ]
}
```

Parse tree:
```
A -> A + M
```

AST:
```json
{
  "name": "+",
  "children": [
    <left operand>,
    <right operand>
  ]
}
```

## Phase 7: Testing

### Testing Strategy
1. Start with Level 1 test cases (l1t1-l1t4)
2. Compare your output with sample output
3. Fix issues before moving to next level
4. Progress through Level 2, 3, 4
5. Try bonus tests (bpt1, brt1)
6. Challenge: ultra test case

### Debugging Tips
1. Print intermediate results
2. Verify each phase independently:
   - Lexer output correct?
   - Parser output correct?
   - Types correct?
   - AST correct?
3. Use the sample executable to see expected output
4. Test small examples manually first

### Common Errors
- **Lexer**: Missing whitespace handling, keyword vs identifier confusion
- **Parser**: Wrong grammar rule, incorrect stack operations
- **Type Checker**: Missing type propagation, wrong type rules
- **Symbol Table**: Variable not found, shadowing issues
- **AST**: Over-simplification, missing information

## Level-by-Level Checklist

### Level 1
- [ ] Lexer recognizes: `Compute`, `.`, `+`, `*`, `(`, `)`, numbers, booleans
- [ ] Parser builds tree for arithmetic expressions
- [ ] Type checker assigns `num` or `bool` types
- [ ] AST simplifies operators and literals
- [ ] All l1tX tests pass

### Level 2
- [ ] Lexer recognizes: `if`, `then`, `else`, `<`, `=`
- [ ] Parser handles conditional expressions
- [ ] Type checker validates boolean guards and branch types
- [ ] AST represents conditionals correctly
- [ ] All l2tX tests pass

### Level 3
- [ ] Lexer recognizes: `Let`, `be`, `num`, `bool`, identifiers
- [ ] Parser handles variable declarations
- [ ] Symbol table stores variable bindings
- [ ] Type checker looks up variable types
- [ ] AST represents declarations and references
- [ ] All l3tX tests pass

### Level 4
- [ ] Lexer recognizes: `maps`, `to`, `>>`, `,`
- [ ] Parser handles function declarations
- [ ] Symbol table stores function signatures
- [ ] Type checker validates function types and applications
- [ ] AST represents function definitions and calls
- [ ] All l4tX tests pass

## Advanced Topics

### Bonus Features (bpt1, brt1)
- Multi-parameter functions
- Recursive functions
- Complex type checking

### Ultra Challenge
Implement the ultra test case which includes:
- Boolean logic functions
- Arithmetic helper functions
- Comparison functions
All implemented in the language itself!

## Tips for Success

1. **Incremental Development**: Build and test one component at a time
2. **Study the Grammar**: Understand the grammar rules thoroughly
3. **Use the Sample**: Run the sample executable frequently to verify expected behavior
4. **Read the Errors**: Compilation and runtime errors often point to the issue
5. **Test Early and Often**: Don't write too much code before testing
6. **Ask for Help**: If stuck, review the documentation or ask questions
7. **Be Patient**: Compilers are complex; take it step by step

Good luck with your implementation!
