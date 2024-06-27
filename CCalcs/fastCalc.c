#include <stdio.h>

typedef struct {
    int gay_num;
    double gay_precent;
} statistics;

statistics gayPercent ( double *marks, int size ){

    double *theEnd = marks + size,
           counter = 0,
           pass = 10;

    statistics stat;

    for( double *mrk = marks; mrk < theEnd; ++mrk)
        if (*mrk < pass)
            counter++;

    stat.gay_num = counter;
    stat.gay_precent = (counter * 100) / size;

    return stat;
}
