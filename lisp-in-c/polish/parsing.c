#include <stdio.h>
#include <stdlib.h>
#include "mpc.h"

/* If we are compiling on Windows */
#ifdef _WIN32
#include <string.h>

static char buffer[2048];

/* Fake readline function */
char* readline(char* prompt)
{
    fputs(prompt, stdout);
    fgets(buffer, 2048, stdin);
    char* cpy = malloc(strlen(buffer)+1);
    strcpy(cpy, buffer);
    cpy[strlen(cpy)-1] = '\0';
    return cpy;
}

/* Fake add_history function */
void add_history(char* unused) {}
#else
#include <editline/readline.h>
#endif

int main(int argc, char** argv)
{
    mpc_parser_t* Number    = mpc_new("number");
    mpc_parser_t* Operater  = mpc_new("operator");
    mpc_parser_t* Expr      = mpc_new("expr");
    mpc_parser_t* Lispy     = mpc_new("lispy");
    
    /* Print Version and Exit Information */
    puts("Lispy Version 0.0.0.0.1");
    puts("Press Ctrl+c to Exit\n");

    /* In a never ending loop */
    while (1)
    {
        /* Output the prompt  and get input*/
        char* input = readline("lispy> ");

        /* Add input to history */
        add_history(input);

        /* Echo input back to user */
        printf("No you're a %s\n", input);

        /* Free retrieed input */
        free(input);
    }
    
    return 0;
}
