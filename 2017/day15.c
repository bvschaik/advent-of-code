#include <stdio.h>

int solve1(long long a, long long b)
{
    int score = 0;
    for (int i = 0; i < 40000000; i++) {
        a = (a * 16807) % 0x7fffffff;
        b = (b * 48271) % 0x7fffffff;
        if ((a & 0xffff) == (b & 0xffff)) {
            score++;
        }
    }
    return score;
}

int solve2(long long a, long long b)
{
    int score = 0;
    for (int i = 0; i < 5000000; i++) {
        do {
            a = (a * 16807) % 0x7fffffff;
        } while (a & 0x3);
        do {
            b = (b * 48271) % 0x7fffffff;
        } while (b & 0x7);
        if ((a & 0xffff) == (b & 0xffff)) {
            score++;
        }
    }
    return score;
}

int main(void)
{
    long long a = 703;
    long long b = 516;
    printf("Part 1: %d\n", solve1(a, b));
    printf("Part 2: %d\n", solve2(a, b));
    return 0;
}
