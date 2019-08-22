#include <stdio.h>

void for_loop()
{
    for (int i = 0; i < 5; i++)
    {
        puts("Hello, world! from For");
    }
}

void while_loop()
{
    int i = 0;
    while (i < 5)
    {
        puts("Hello, world! from While");
        i = i + 1;
    }
}

void user_loop(int loop_size)
{
    for (int i = 0; i < loop_size; i++)
    {
        puts("Hello, world! user loop");
    }
}
    
int main(int argc, char** argv)
{
    puts("Hello, world!");
    for_loop();
    while_loop();
    user_loop(7);
    return 0;
}