
int fib(int n) {
  if (n < 3) {
    return 1;
  } else {
    return fib(n-2) + fib(n-1);
  }
}
