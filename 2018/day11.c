#include <stdio.h>

#define SIZE 300
#define SERIAL (9798 % 1000)

int matrix_1[SIZE][SIZE];
int matrix_xn[SIZE][SIZE]; // matrix with sums of horizontal 'bricks' of n x 1
int matrix_yn[SIZE][SIZE]; // matrix with sums of vertical 'bricks' of n x 1
int matrix_nn[SIZE][SIZE]; // matrix with sums of squares n x n

int get_fuel(int x, int y) {
    int rack = x + 10;
    int power = (rack * y + SERIAL) * rack;
    power = ((power % 1000) / 100) - 5; // you end up with a number between -5 and 4
    return power;
}

void solve1(void) {
    int matrix[SIZE][SIZE];
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++) {
            matrix[y][x] = get_fuel(x + 1, y + 1);
        }
    }

    // Calculate for for every row: sum of [x x+1 x+2]
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE - 2; x++) {
            matrix[y][x] += matrix[y][x+1] + matrix[y][x+2];
        }
    }

    // Calculate for every column: sum of [y y+1 y+2]
    for (int x = 0; x < SIZE - 2; x++) {
        for (int y = 0; y < SIZE - 2; y++) {
            matrix[y][x] += matrix[y+1][x] + matrix[y+2][x];
        }
    }

    int max_value = 0;
    int max_coord[2];
    for (int x = 0; x < SIZE - 2; x++) {
        for (int y = 0; y < SIZE - 2; y++) {
            if (matrix[y][x] > max_value) {
                max_value = matrix[y][x];
                max_coord[0] = x + 1;
                max_coord[1] = y + 1;
            }
        }
    }
    printf("%d,%d\n", max_coord[0], max_coord[1]);
}

void solve2(void) {
    int max_value = 0;
    int max_coord[3];

    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++) {
            int value = matrix_nn[y][x] = matrix_xn[y][x] = matrix_yn[y][x] = matrix_1[y][x] = get_fuel(x + 1, y + 1);
            if (value > max_value) {
                max_value = value;
                max_coord[0] = x + 1;
                max_coord[1] = y + 1;
                max_coord[2] = 1;
            }
        }
    }

    /*
     * Dynamic programming solution: squares n x n are calculated by the sum of:
     * - square (n-1) x (n-1) at (x, y)
     * - vertical brick of n x 1 starting at (x + offset, y)
     * - horizontal brick of n x 1 starting at (x, y + offset)
     * - single item at (x + offset, y + offset)
     * Time complexity: O(n^3)
     */
    for (int offset = 1; offset < SIZE - 1; offset++) {
        int iters = 300 - offset;

        // Calculate bricks
        for (int y = 0; y < iters; y++) {
            for (int x = 0; x < iters; x++) {
                matrix_xn[y][x] += matrix_1[y][x + offset];
                matrix_yn[y][x] += matrix_1[y + offset][x];
            }
        }
        // Calculate n x n squares
        for (int y = 0; y < iters; y++) {
            for (int x = 0; x < iters; x++) {
                int value = matrix_nn[y][x] = matrix_nn[y][x] + matrix_xn[y+offset][x] + matrix_yn[y][x+offset] + matrix_1[y+offset][x+offset];
                if (value > max_value) {
                    max_value = value;
                    max_coord[0] = x + 1;
                    max_coord[1] = y + 1;
                    max_coord[2] = offset + 1;
                }
            }
        }
    }
    printf("%d,%d,%d\n", max_coord[0], max_coord[1], max_coord[2]);
}

int main(void) {
    solve1();
    solve2();
    return 0;
}
