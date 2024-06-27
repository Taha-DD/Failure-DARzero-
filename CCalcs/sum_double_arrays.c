#include <stdio.h>
void sum_double_arrays(double* a, double* b, double* c, int size) {
    for (int i = 0; i < size; i++) {
        c[i] = (a[i] * 26 + b[i] * 31) / 57;
    }
}
