#include <stdio.h>

#define MAX_VALUE 1000000
#define MAX_INITIAL 9

struct {
    int nodes[MAX_VALUE + 1];
    int max_value;
    int current;
} ring;

void init(const char *initial, int max_value)
{
    ring.max_value = max_value;
    int prev = max_value <= MAX_INITIAL ? initial[MAX_INITIAL-1] : max_value;
    for (int i = 0; i < MAX_INITIAL; i++) {
        int n = initial[i] - '0';
        ring.nodes[prev] = n;
        prev = n;
    }
    for (int n = MAX_INITIAL + 1; n <= MAX_VALUE; n++) {
        ring.nodes[prev] = n;
        prev = n;
    }
    ring.current = initial[0] - '0';
}

void move(int times)
{
    for (int i = 0; i < times; i++) {
        int n1 = ring.nodes[ring.current];
        int n2 = ring.nodes[n1];
        int n3 = ring.nodes[n2];
        int next_value = ring.current;
        while (1) {
            next_value = next_value == 1 ? ring.max_value : next_value - 1;
            if (next_value != n1 && next_value != n2 && next_value != n3) {
                break;
            }
        }
        ring.nodes[ring.current] = ring.nodes[n3];
        ring.nodes[n3] = ring.nodes[next_value];
        ring.nodes[next_value] = n1;
        ring.current = ring.nodes[ring.current];
    }
}

int solution1(void)
{
    int n = ring.nodes[1];
    int result = 0;
    while (n != 1) {
        result = result * 10 + n;
        n = ring.nodes[n];
    }
    return result;
}

long long solution2(void)
{
    return (long long) ring.nodes[1] * ring.nodes[ring.nodes[1]];
}

int main()
{
    init("871369452", MAX_VALUE);
    move(10000000);
    printf("%lld\n", solution2());
    return 0;
}
