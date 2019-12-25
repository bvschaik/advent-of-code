import adventofcode

REVERSE = 0
CUT = 1
DEAL = 2

def modpow(base, power, mod):
    powers = [base]
    p2 = 2
    while p2 < power:
        last = powers[-1]
        powers.append((last * last) % mod)
        p2 *= 2

    result = 1
    bit = 0
    while power > 0:
        if power & 1:
            result = (result * powers[bit]) % mod
        power = power >> 1
        bit += 1
    return result

# Function to find modulo inverse of b
def modinv(b, m): 
    # If b and m are relatively prime,  
    # then modulo inverse is b^(m-2) mode m  
    return modpow(b, m - 2, m) 
  
# compute a / b % m  
def moddiv(a, b, m): 
    inv = modinv(b,m)
    return (inv * a) % m

def get_deal_increment(deal, size):
    offset = deal - size % deal # the first wrapped-around number will end up at this offset
    value = size // deal + 1 # the value of the first wrapped-around number
    # We need to calculate: offset * x == value (mod size)
    # --> x = offset^-1 * value (mod size)
    return (modinv(offset, size) * value) % size

class deck:
    def __init__(self, size):
        self.deck = list(range(size))

    def reverse(self):
        self.deck.reverse()

    def cut(self, n):
        self.deck = self.deck[n:] + self.deck[:n]

    def deal(self, n):
        total = len(self.deck)
        new_deck = [0] * total
        offset = 0
        for i in self.deck:
            new_deck[offset] = i
            offset = (offset + n) % total
        self.deck = new_deck

    def print(self):
        print(self.deck)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.commands = []

    def input_line(self, line):
        if line == 'deal into new stack':
            self.commands.append((REVERSE, 0))
        elif line.startswith('cut '):
            self.commands.append((CUT, int(line[4:])))
        elif line.startswith('deal with increment '):
            self.commands.append((DEAL, int(line[20:])))
        else:
            print("Unknown command:", line)

    def solve1(self):
        size = 10007
        (deal, cut) = self.simplify(self.commands, size)
        d = deck(size)
        d.deal(deal)
        d.cut(cut)
        return str(d.deck.index(2019))

    def solve2(self):
        size = 119315717514047
        times = 101741582076661
        (deal, cut) = self.simplify(self.commands, size)

        # Executing commands multiple times:
        # Times 2:
        # - deal = (deal * deal) mod size
        # - cut = (cut * deal + cut) mod size
        # Times 3:
        # - deal = (deal * deal) * deal mod size
        # - cut = (cut * deal + cut) * deal + cut mod size = cut * (deal^2 + deal + 1)
        # Times n:
        # total_deal = deal^n mod size
        # total_cut = cut * deal^n-1 + cut * deal^n-2 + ... + cut * deal + cut mod size
        #           = cut * (deal^n-1 + deal^n-2 + ... + deal + 1) mod size
        #           = cut * (deal^n - 1) / (deal - 1)) mod size
        total_deal = modpow(deal, times, size)
        total_cut = (cut * moddiv(total_deal - 1, deal - 1, size)) % size

        # Calculate the requested position before the cut operation:
        requested_position = (2020 + total_cut) % size

        # Now we just need to find out where this number comes from during deal...
        # Deal will result in 0......1......2......3.. in chunks of size 'deal'
        # The value in each chunk is offset by the chunk id
        chunk_id = requested_position // total_deal
        # The requested position's offset within the chunk:
        offset_in_chunk = requested_position % total_deal

        # Every element in the chunk is the previous element plus some increment
        deal_increment = get_deal_increment(total_deal, size)

        value = (chunk_id + offset_in_chunk * deal_increment) % size
        return str(value)

    def simplify(self, commands, size):
        # Rules:
        # reverse() = deal(size - 1) + cut(1)
        # cut(n) + cut(m) = cut(n + m)
        # cut(n) + deal(m) = deal(m) + cut(n * m)
        # deal(n) + deal(m) = deal(n * m)
        current_cut = 0
        current_deal = 1
        for c, n in commands:
            if c == REVERSE:
                current_deal = (current_deal * (size - 1)) % size
                current_cut = (current_cut * (size - 1) + 1) % size
            elif c == CUT:
                current_cut = (current_cut + n) % size
            elif c == DEAL:
                current_deal = (current_deal * n) % size
                current_cut = (current_cut * n) % size

        return (current_deal, current_cut)

    def run_commands(self, commands, size):
        d = deck(size)
        for c, n in commands:
            if c == REVERSE:
                d.reverse()
            elif c == CUT:
                d.cut(n)
            elif c == DEAL:
                d.deal(n)
        return d.deck

r = runner()

r.run()
