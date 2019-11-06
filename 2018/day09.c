#include <stdio.h>

#define MAX_NODES 7200000
#define MAX_PLAYERS 500

typedef struct node_t {
    int id;
    struct node_t *prev;
    struct node_t *next;
} node;

node nodes[MAX_NODES];
unsigned long long scores[MAX_PLAYERS];

void init(void) {
    for (int i = 0; i < MAX_NODES; i++) {
        nodes[i].id = i;
    }
}

node* insert_after(node *self, node *n) {
    self->next = n->next;
    self->prev = n;
    n->next->prev = self;
    n->next = self;
    return self;
}

node* remove_node(node *self) {
    self->prev->next = self->next;
    self->next->prev = self->prev;
    return self->next;
}

void run(int marbles, int players) {
    init();

    node *current = &nodes[0];
    current->prev = current;
    current->next = current;

    for (int m = 1; m <= marbles; m++) {
        if (m % 23 == 0) {
            for (int p = 0; p < 7; p++) {
                current = current->prev;
            }
            scores[m % players] += m + current->id;
            current = remove_node(current);
        } else {
            current = insert_after(&nodes[m], current->next);
        }
    }

    unsigned long long max = 0;
    for (int i = 0; i < players; i++) {
        if (scores[i] > max) {
            max = scores[i];
        }
    }
    printf("%llu\n", max);
}

int main(int argc, char **argv) {
    run(7173000, 464);

    return 0;
}
