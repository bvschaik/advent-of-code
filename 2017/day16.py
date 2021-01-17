import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.moves = []

    def input_line(self, line):
        for m in line.split(','):
            if m[0] == 's':
                self.moves.append(('s', int(m[1:])))
            elif m[0] == 'x':
                (p1, p2) = map(int, m[1:].split('/'))
                self.moves.append(('x', (p1, p2)))
            elif m[0] == 'p':
                (d1, d2) = m[1:].split('/')
                self.moves.append(('p', (d1, d2)))

    def solve1(self):
        lineup = [chr(ord('a') + x) for x in range(16)]
        for m, v in self.moves:
            if m == 's':
                spin = v
                lineup = lineup[16-spin:] + lineup[0:16-spin]
            elif m == 'x':
                (p1, p2) = v
                tmp = lineup[p1]
                lineup[p1] = lineup[p2]
                lineup[p2] = tmp
            elif m == 'p':
                (d1, d2) = v
                index1 = lineup.index(d1)
                index2 = lineup.index(d2)
                lineup[index1] = d2
                lineup[index2] = d1

        return ''.join(lineup)

    def solve2(self):
        # Reduce the input to a list of independent partner operations,
        # a list of exchanges and a global spin to be applied at the end
        partner = []
        exchange = []
        spin = 0

        for m, v in self.moves:
            if m == 'p':
                partner.append(v)
            elif m == 's':
                spin = (spin + v) % 16
            elif m == 'x':
                exchange.append(((v[0] - spin) % 16, (v[1] - spin) % 16))

        times = 1000000000
        lineup = [chr(ord('a') + x) for x in range(16)]

        exchange_spin_values = self.get_exchange_spin_values(lineup, exchange, spin)
        lineup = list(exchange_spin_values[times % len(exchange_spin_values)])

        partner_values = self.get_partner_values(lineup, partner)
        final = partner_values[times % len(partner_values)]

        return final

    def get_exchange_spin_values(self, lineup, exchange, spin):
        results = [''.join(lineup)]
        while True:
            for a, b in exchange:
                tmp = lineup[a]
                lineup[a] = lineup[b]
                lineup[b] = tmp
            lineup = lineup[16-spin:] + lineup[0:16-spin]
            result = ''.join(lineup)
            if result == results[0]:
                break
            results.append(result)
        return results

    def get_partner_values(self, lineup, partner):
        results = [''.join(lineup)]
        while True:
            for d1, d2 in partner:
                index1 = lineup.index(d1)
                index2 = lineup.index(d2)
                lineup[index1] = d2
                lineup[index2] = d1
            result = ''.join(lineup)
            if result == results[0]:
                break
            results.append(result)
        return results

r = runner()

r.run()
