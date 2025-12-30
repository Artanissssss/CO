gcc lexer.c -c
gcc symbol_table.c -c
gcc parser.c -c
gcc type_checker.c -c
gcc ast_gen.c -c
gcc lib.c -c
gcc main.c lexer.o symbol_table.o parser.o type_checker.o ast_gen.o lib.o -o fun.exe
fun sample
pause
del *.o