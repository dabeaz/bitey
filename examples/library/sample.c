#include <stdio.h>

extern int fib(int n);

void print_fib(int n) {
  while (n > 0) {
    printf("%d\n", fib(n));
    n--;
  }
}


