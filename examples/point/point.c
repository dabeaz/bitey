#include <math.h>

struct Point {
  double x;
  double y;
};

double distance(struct Point *p1, struct Point *p2) {
  return sqrt((p1->x - p2->x)*(p1->x - p2->x) + 
	      (p1->y - p2->y)*(p1->y - p2->y));
}


