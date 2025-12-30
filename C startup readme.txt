This folder contains all the .c and .h files that you need to implement.
-	"main.c": the main entry of your program
	+	It is executed with an argument, which specifies the name of source code file that will be analyzed.
	+	It only makes function calls to parser, but does not do any process on the source code.

-	"lexer.h" and "lexer.c": the implementation of the lexer

-	"parser.h" and "parser.c": the implementation of the parser

-	"type_checker.h" and "type_checker.c": the implementation of the type checker

-	"ast_gen.h" and "ast_gen.c": the implementation of the AST generation

-	"symbol_table.h" and "symbol_table.c": the implementation of the symbol table

-	"lib.h" and "lib.c": the file contains all other functions that you want to implement

The folder also contains:
-	"sample": an empty file only for demonstration of the main function with arguments

-	"make.bat": Windows environment makefile, which contains all the compilation and execution command. Your submission will be compiled by the same makefile. Thus,
	
	DO NOT CHANGE ANY FILE NAME!
	DO NOT CHANGE ANY FILE NAME!
	DO NOT CHANGE ANY FILE NAME!
	DO NOT CHANGE ANY FILE NAME!

This file structure is only a suggestion from Goliath. Students of course have the freedome to implement the project in their own way. For example, all features are implemented in "main.c".