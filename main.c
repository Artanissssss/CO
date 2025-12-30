#include<stdio.h>
#include"lexer.h"
#include"symbol_table.h"
#include"parser.h"
#include"type_checker.h"
#include"ast_gen.h"
#include"lib.h"

int main(int argc, char *argv[]){
	printf("The input file is %s\n",argv[1]);
	symbol_table_test();
	lexer_test();
	parser_test();
	type_checker_test();
	ast_gen_test();
	lib_test();
	return 0;
}