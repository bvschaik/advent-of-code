import adventofcode
from collections import defaultdict

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = line

    def solve1(self):
        width = 25
        height = 6
        size = width * height
        layers = []
        
        layer = -1
        min_zeroes = size
        min_layer = -1
        for i, c in enumerate(self.data):
            if i % size == 0:
                if layer >= 0 and layers[layer][0] < min_zeroes:
                    min_zeroes = layers[layer][0]
                    min_layer = layer
                layer += 1
                layers.append([0, 0, 0])
            value = int(c)
            layers[layer][value] += 1
        
        return str(layers[min_layer][1] * layers[min_layer][2])

    def solve2(self):
        width = 25
        height = 6
        size = width * height
        layers = [self.data[i:i+150] for i in range(0, len(self.data), size)]
        # print(layers)

        for i in range(size):
            val = TRANSPARENT
            for p in layers:
                pval = p[i]
                if pval == BLACK or pval == WHITE:
                    val = pval
                    break
            if val == BLACK:
                print(' ', end = '')
            elif val == WHITE:
                print('#', end = '')
            else:
                print(val, end = '')
            if (i + 1) % width == 0:
                print()
        return 'see above'

r = runner()

r.run()
