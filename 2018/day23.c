#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MAX_BOTS 1000
#define SPLIT_PARTS 8

typedef struct {
    int x;
    int y;
    int z;
} position;

typedef struct {
    position pos;
    int r;
} nanobot;

typedef struct {
    position center;
    int r;
    int bots_in_range;
} cube;

static int total_bots;
static nanobot bots[MAX_BOTS];

static struct {
    int max_bots;
    position max_pos;
} search;

int distance_between(const position *a, const position *b)
{
    return abs(a->x - b->x) + abs(a->y - b->y) + abs(a->z - b->z);
}

int distance_to_origin(const position *p)
{
    return abs(p->x) + abs(p->y) + abs(p->z);
}

void position_translate(position *p, int dx, int dy, int dz)
{
    p->x += dx;
    p->y += dy;
    p->z += dz;
}

int nanobot_in_range(const nanobot *bot, const position *pos)
{
    return distance_between(&bot->pos, pos) <= bot->r;
}

int min_axis_dist(int target, int a_min, int a_max)
{
    if (target < a_min) {
        return a_min - target;
    } else if (target > a_max) {
        return target - a_max;
    } else {
        return 0;
    }
}

int cube_intersects_bot(const cube *c, const nanobot *bot)
{
    if (c->r == 0) {
        return nanobot_in_range(bot, &c->center);
    }
    // Calculate minimum distance required to travel along each axis to
    // arrive at the bounding box. Sum to find the Manhattan distance.
    int distance =
        min_axis_dist(bot->pos.x, c->center.x - c->r, c->center.x + c->r - 1) +
        min_axis_dist(bot->pos.y, c->center.y - c->r, c->center.y + c->r - 1) +
        min_axis_dist(bot->pos.z, c->center.z - c->r, c->center.z + c->r - 1);
    return distance <= bot->r;
}

void init_cube(cube *c)
{
    int in_range = 0;
    for (int i = 0; i < total_bots; i++) {
        if (cube_intersects_bot(c, &bots[i])) {
            in_range++;
        }
    }
    c->bots_in_range = in_range;
    //printf("Cube: bots in range = %d\n", c->bots_in_range);
}

int sort_by_bots(const void *a, const void *b)
{
    const cube *ca = (cube *) a;
    const cube *cb = (cube *) b;
    return cb->bots_in_range - ca->bots_in_range;
}

int split_cube(const cube *c, cube *parts)
{
    if (c->r == 0) {
        return 0;
    }
    int new_r = c->r / 2;
    int low = new_r > 0 ? -new_r : -1;
    int high = new_r;
    for (int i = 0; i < SPLIT_PARTS; i++) {
        parts[i].r = new_r;
        parts[i].center = c->center;
    }
    position_translate(&parts[0].center, low, low, low);
    position_translate(&parts[1].center, low, low, high);
    position_translate(&parts[2].center, low, high, low);
    position_translate(&parts[3].center, low, high, high);
    position_translate(&parts[4].center, high, low, low);
    position_translate(&parts[5].center, high, low, high);
    position_translate(&parts[6].center, high, high, low);
    position_translate(&parts[7].center, high, high, high);
    int valid_parts = 0;
    for (int i = 0; i < SPLIT_PARTS; i++) {
        init_cube(&parts[i]);
        if (parts[i].bots_in_range > 0) {
            valid_parts++;
        }
    }
    qsort(parts, SPLIT_PARTS, sizeof(cube), sort_by_bots);
    return valid_parts;
}

void update_search_state(const cube *c)
{
    if (c->r != 0 || c->bots_in_range < search.max_bots) {
        return;
    }
    if (c->bots_in_range > search.max_bots) {
        // printf("Updating max to %d\n", c->bots_in_range);
        search.max_bots = c->bots_in_range;
        search.max_pos = c->center;
    } else if (distance_to_origin(&c->center) < distance_to_origin(&search.max_pos)) {
        search.max_pos = c->center;
    }
}

void do_search(const cube *cubes, int size)
{
    cube parts[SPLIT_PARTS];
    for (int i = 0; i < size; i++) {
        const cube *c = &cubes[i];
        if (c->bots_in_range > search.max_bots) {
            update_search_state(c);
            int num_parts = split_cube(c, parts);
            do_search(parts, num_parts);
        }
    }
}

int solve2(void)
{
    search.max_bots = 0;
    cube start = {{0, 0, 0}, 1 << 30};
    init_cube(&start);

    do_search(&start, 1);

    return distance_to_origin(&search.max_pos);
}

void read_input(void)
{
    int x, y, z, r;
    while (scanf("pos=<%d,%d,%d>, r=%d\n", &x, &y, &z, &r) == 4) {
        bots[total_bots].pos.x = x;
        bots[total_bots].pos.y = y;
        bots[total_bots].pos.z = z;
        bots[total_bots].r = r;
        total_bots++;
    }
}

int main(int argc, char **argv)
{
    read_input();

    int result = solve2();
    printf("Solution 2: %d\n", result);    

    return 0;
}