/* A function that determines if an integer is a prime number or not.
   This is just a naive implementation--there are faster ways to do it */

int isprime(int n) {
  int factor = 3;
  /* Special case for 2 */
  if (n == 2) {
    return 1;
  }
  /* Check for even numbers */
  if ((n % 2) == 0) {
    return 0;
  }
  /* Check for everything else */
  while (factor*factor < n) {
    if ((n % factor) == 0) {
      return 0;
    }
    factor += 2;
  }
  return 1;
}

