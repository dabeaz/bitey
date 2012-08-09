#include <math.h>

/* Tests of various C argument types */

char add_char(char x, char y) {
  return x+y;
}

short add_short(short x, short y) {
  return x+y;
}

int add_int(int x, int y) {
  return x+y;
}

long add_long(long x, long y) {
  return x+y;
}

long long add_longlong(long long x, long long y) {
  return x+y;
}

float add_float(float x, float y) {
  return x+y;
}

double add_double(double x, double y) {
  return x+y;
}

void mutate_int(int *x) {
  *x *= 2;
}

void mutate_short(short *x) {
  *x *= 2;
}

void mutate_long(long *x) {
  *x *= 2;
}

void mutate_longlong(long long *x) {
  *x *= 2;
}

void mutate_float(float *x) {
  *x *= 2;
}

void mutate_double(double *x) {
  *x *= 2;
}

/* Some tests of C arrays */

int arr_sum_int(int x[4]) {
  int total = 0;
  int n;
  for (n = 0; n < 4; n++) {
    total += x[n];
  }
  return total;
}

double arr_sum_double(double x[4]) {
  double total = 0;
  int n;
  for (n = 0; n < 4; n++) {
    total += x[n];
  }
  return total;
}

typedef struct Point {
  double x;
  double y;
} Point;

double distance(struct Point *p1, Point *p2) {
  return hypot(p1->x - p2->x, p1->y - p2->y);
}

