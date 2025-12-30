# Quick Start Guide

This is a quick reference for getting started with the COMP3173 Compiler Project.

## 📋 Before You Begin

1. **Choose your implementation language**:
   - 🐍 Python (easiest - recommended for beginners)
   - ☕ Java (moderate difficulty)
   - 🔧 C (hardest - full control)

2. **Read the documentation** (in order):
   - Start with `README.md` for project overview
   - Read `LANGUAGE_SPEC.md` to understand the language
   - Follow `IMPLEMENTATION_GUIDE.md` for implementation steps

## 🚀 Quick Start

### Python
```bash
python3 main.py l1t1
```

### Java
```bash
javac *.java
java Main l1t1
```

### C
```bash
gcc main.c lexer.c symbol_table.c parser.c type_checker.c ast_gen.c lib.c -o fun.exe
./fun.exe l1t1
```

## 📊 Project Phases

The project consists of **4 levels** that must be completed in order:

| Level | Features | Test Cases |
|-------|----------|------------|
| **Level 1** | Basic arithmetic (`+`, `*`), numbers, booleans | l1t1 - l1t4 |
| **Level 2** | Conditionals (`if-then-else`), comparisons (`<`, `=`) | l2t1 - l2t4 |
| **Level 3** | Variable declarations (`Let num x be ...`) | l3t1 - l3t4 |
| **Level 4** | Function declarations and applications | l4t1 - l4t4 |

## 🔧 Components to Implement

Each level requires implementing these components:

1. **Lexer** → Tokenizes input → outputs `*_lexer.json`
2. **Parser** → Builds parse tree → outputs `*_parse.json`
3. **Type Checker** → Validates types → outputs `*_type.json`
4. **AST Generator** → Simplifies tree → outputs `*_ast.json`
5. **Symbol Table** → Manages variables (Level 3+)

## 📁 Important Files

### Documentation
- `README.md` - Project overview
- `LANGUAGE_SPEC.md` - Language syntax and semantics
- `IMPLEMENTATION_GUIDE.md` - Step-by-step instructions
- `QUICK_START.md` - This file

### Grammar Files
- `level1_grammar.txt` - Basic arithmetic grammar
- `level2_grammar.txt` - Adds conditionals
- `level3_grammar.txt` - Adds variables
- `level4_grammar.txt` - Adds functions

### Parsing Tables
- `level1_parsing_table.csv`
- `level2_parsing_table.csv`
- `level3_parsing_table.csv`
- `level4_parsing_table.csv`

### Type Rules
- `level1_type_rule.txt` - Type checking rules (Level 1)

### Your Implementation Files

**Python**:
- `main.py` - Entry point
- `lexer.py` - Your lexer implementation

**Java**:
- `Main.java` - Entry point
- `Lexer.java` - Your lexer implementation (add more files as needed)

**C**:
- `main.c` - Entry point
- `lexer.c` / `lexer.h` - Lexer
- `parser.c` / `parser.h` - Parser
- `type_checker.c` / `type_checker.h` - Type checker
- `ast_gen.c` / `ast_gen.h` - AST generator
- `symbol_table.c` / `symbol_table.h` - Symbol table
- `lib.c` / `lib.h` - Utility functions

## 🎯 Testing Your Implementation

### Use the Sample Executable
```bash
# Linux/macOS
chmod +x sample_linux.exe
./sample_linux.exe l1t1

# Windows
sample_windows.exe l1t1
```

This generates the expected output files that you can compare against.

### Test Cases by Level

**Level 1** (Basic Arithmetic):
```
Compute 1 .
Compute true .
Compute 1 + 1 .
Compute ( 1 + 2 ) * 3 .
```

**Level 2** (Conditionals):
```
Compute if true then 1 else 2 .
Compute if 1 = 1 then 1 else 2 .
```

**Level 3** (Variables):
```
Let num a be 1 .
Compute a .
```

**Level 4** (Functions):
```
Let num >> num suc maps x to x + 1 .
Compute suc 5 .
```

## ⚠️ Important Rules

1. **DO NOT change file names** - The autograder expects specific names
2. **NO external libraries** - Only use standard library
3. **Complete levels in order** - Don't skip ahead
4. **Test frequently** - Test after each component

## 🐛 Common Issues

### Lexer Issues
- Forgetting to skip whitespace
- Not recognizing keywords before identifiers
- Missing token types

### Parser Issues
- Wrong shift/reduce actions
- Incorrect stack operations
- Not building parse tree correctly

### Type Checker Issues
- Forgetting to propagate types
- Wrong type rules
- Not handling TYPE_ERROR

### Symbol Table Issues (Level 3+)
- Variable not declared before use
- Not handling scope correctly

## 💡 Tips for Success

1. **Start small** - Test with simple examples first
2. **Use the sample** - Compare your output with sample output
3. **Debug incrementally** - Fix one component at a time
4. **Read error messages** - They often tell you exactly what's wrong
5. **Ask for help** - Don't struggle alone

## 🎓 Bonus Challenges

After completing all 4 levels:
- `bpt1` - Multi-parameter functions
- `brt1` - Recursive functions
- `ultra` - Complex program demonstrating language capabilities

## 📚 Example Language Programs

### Factorial Function
```
Let num >> num factorial maps x to 
    if x = 1 then 
        1 
    else 
        x * factorial ( x + ( 0 - 1 ) ) .
Compute factorial 5 .
```

### Addition Function (2 parameters)
```
Let num , num >> num add maps a , b to a + b .
Compute add 3 4 .
```

### Boolean Logic
```
Let bool , bool >> bool and maps a , b to 
    if a then b else false .
```

## 🔗 Next Steps

1. ✅ Read `README.md`
2. ✅ Study `LANGUAGE_SPEC.md`
3. ✅ Follow `IMPLEMENTATION_GUIDE.md`
4. ✅ Start with Level 1
5. ✅ Test frequently
6. ✅ Progress to higher levels
7. ✅ Challenge yourself with bonus tests

Good luck! 🚀
