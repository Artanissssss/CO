# Language Specification

## Introduction

This document describes the syntax and semantics of a simple functional programming language designed for mathematical expressions. The language supports numbers, booleans, arithmetic operations, conditional expressions, variable declarations, and function definitions.

## Lexical Elements

### Keywords
- `Compute` - Marks the computation statement
- `Let` - Variable or function declaration
- `be` - Assignment in variable declaration
- `maps` - Function parameter list introducer
- `to` - Function body introducer
- `if`, `then`, `else` - Conditional expression
- `num` - Number type
- `bool` - Boolean type

### Literals
- **Number Literals** (`num_lit`): Integer values (e.g., `1`, `42`, `100`)
- **Boolean Literals** (`bool_lit`): `true` or `false`

### Operators
- **Arithmetic**: `+` (addition), `*` (multiplication)
- **Relational**: `<` (less than), `=` (equality)
- **Type Arrow**: `>>` (function type separator)

### Delimiters
- `(` `)` - Parentheses for grouping
- `,` - Parameter separator
- `.` - Statement terminator

### Identifiers
- **id**: Variable and function names (e.g., `x`, `add`, `factorial`)
- Must start with a letter
- Can contain letters and numbers

## Grammar Evolution

The language is defined in four levels of increasing complexity:

### Level 1: Basic Arithmetic

Grammar rules:
```
E -> A                  (Expression is Arithmetic)
A -> A + M              (Addition)
A -> M                  (Single Multiplicative)
M -> M * U              (Multiplication)
M -> U                  (Single Unary)
U -> P                  (Unary is Primary)
P -> num_lit            (Number literal)
P -> bool_lit           (Boolean literal)
P -> ( E )              (Parenthesized expression)
C -> Compute E .        (Computation statement)
```

Example programs:
```
Compute 1 .
Compute true .
Compute 1 + 1 .
Compute ( 1 + 2 ) * 3 .
```

### Level 2: Conditional Expressions

Adds if-then-else and relational operators:
```
E -> if B then A else A    (Conditional expression)
E -> A                     (Arithmetic expression)
B -> P < P                 (Less than)
B -> P = P                 (Equality)
B -> P                     (Boolean value)
```

Example programs:
```
Compute if true then 1 else 2 .
Compute if 1 = 1 then 1 else 2 .
Compute if 3 < 5 then 10 else 20 .
```

### Level 3: Variable Declarations

Adds variable declarations and references:
```
L -> S C                       (Statements followed by Computation)
S -> S D                       (Multiple declarations)
S -> D                         (Single declaration)
D -> Let T id be E .          (Variable declaration)
T -> num                       (Number type)
T -> bool                      (Boolean type)
P -> id                        (Variable reference)
```

Example programs:
```
Let num a be 1 .
Compute a .
```

```
Let num x be 5 .
Let num y be x + 3 .
Compute y * 2 .
```

### Level 4: Function Declarations and Applications

Adds function definitions and function calls:
```
D -> Let F id maps I to E .    (Function declaration)
F -> G >> T                    (Function type)
G -> T , G                     (Multiple parameter types)
G -> T                         (Single parameter type)
I -> id , I                    (Multiple parameters)
I -> id                        (Single parameter)
U -> U P                       (Function application)
```

Example programs:
```
Let num >> num suc maps x to x + 1 .
Compute suc 5 .
```

```
Let num , num >> num add maps a , b to a + b .
Compute add 3 4 .
```

```
Let num >> num factorial maps x to 
    if x = 1 then 
        1 
    else 
        x * factorial ( x + ( 0 - 1 ) ) .
Compute factorial 5 .
```

## Type System

### Basic Types
- `num` - Integer type
- `bool` - Boolean type

### Function Types
- `T1 >> T2` - Function from T1 to T2
- `T1 , T2 >> T3` - Function from (T1, T2) to T3

### Type Rules (Level 1 Example)

Addition rule:
```
A1 -> A2 + M
if A2.type == num and M.type == num then
    A1.type := num
else
    A1.type := TYPE_ERROR
```

Multiplication rule:
```
M1 -> M2 * U
if M2.type == num and U.type == num then
    M1.type := num
else
    M1.type := TYPE_ERROR
```

Number literal:
```
P -> num_lit
P.type := num
```

Boolean literal:
```
P -> bool_lit
P.type := bool
```

## Semantics

### Evaluation Order
1. Parse the source code into a parse tree
2. Check types according to type rules
3. Generate an Abstract Syntax Tree (AST)
4. Evaluate the AST

### Scoping Rules
- Variables must be declared before use
- Functions can be recursive
- Later declarations shadow earlier ones with the same name

### Function Application
- Functions are applied using juxtaposition: `f x` means "apply f to x"
- Multi-argument functions use currying: `add 1 2` is `(add 1) 2`

## Advanced Examples

### Boolean Operations
```
Let bool , bool >> bool conj maps a , b to 
    if a then b else false .

Let bool , bool >> bool disj maps a , b to 
    if a then true else b .

Let bool >> bool negb maps a to 
    if a then false else true .
```

### Arithmetic Functions
```
Let num >> num pred maps x to x + ( 0 - 1 ) .

Let num , num >> num subtract maps a , b to 
    if b = 0 then a else subtract ( pred a ) ( pred b ) .
```

### Comparison Functions
```
Let num , num >> bool les maps a , b to 
    if a < b then true else false .

Let num , num >> bool eq maps a , b to 
    if a = b then true else false .
```

## Language Limitations

1. **No negative number syntax**: Use `0 - x` instead of `-x`
2. **No subtraction operator**: Must implement via function (see the `subtract` function in [Advanced Examples](#advanced-examples) section)
3. **No division operator**: Must implement via recursive function (see `div` and `divhp` examples in the `ultra` test file)
4. **Limited relational operators**: Only `<` and `=` are built-in (see `les`, `eq`, `gtr` functions in [Advanced Examples](#advanced-examples))
5. **No string type**: Only numbers and booleans
6. **No loops**: Use recursion instead (see function examples in Level 4)
7. **No mutable state**: All values are immutable

## Error Conditions

### Lexical Errors
- Invalid characters
- Malformed number literals

### Syntax Errors
- Missing delimiters (parentheses, periods)
- Incorrect keyword usage
- Invalid expression structure

### Type Errors
- Type mismatch in arithmetic operations (e.g., `1 + true`)
- Type mismatch in relational operations
- Type mismatch in conditional (guard must be bool)
- Wrong number of function arguments
- Function application to non-function

### Semantic Errors
- Undefined variable reference
- Undefined function reference
- Circular type dependencies

## Output Format

All implementations must produce JSON output for each phase:

1. **Lexer Output** (`*_lexer.json`): Array of tokens
2. **Parser Output** (`*_parse.json`): Parse tree
3. **Type Checker Output** (`*_type.json`): Parse tree with type annotations
4. **AST Output** (`*_ast.json`): Simplified abstract syntax tree

See the sample executables for exact output format examples.
