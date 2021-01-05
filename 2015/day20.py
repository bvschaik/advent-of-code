import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(20)

    def reset(self):
        self.min_presents = 0

    def input_line(self, line):
        self.min_presents = int(line)

    def solve1(self):
        # The value we're looking for is the sum of divisors of N (inclusive)
        # The sum of divisors can be calculated using the prime factorization:
        # sum_of_divisors(p^a) = sum of p^0 + p^1 + p^2 + ... + p^n
        # sum_of_divisors(p^a * q^b) = sum_of_divisors(p^a) * sum_of_divisors(p^b)
        # The lowest number with the most divisors only has a few small primes as factors
        # So pre-calculate some p^a values to be used later
        primes = [2, 3, 5, 7, 11, 13]
        max_times = []
        for p in primes:
            divisors = 1
            value = 1
            power = 1
            powers = [1]
            while divisors < self.min_presents // 10:
                value *= p
                divisors += value
                powers.append(divisors)
            max_times.append(powers)

        self.global_min = self.min_presents
        self.recurse(primes, max_times, 0, 1, 10)
        return str(self.global_min)

    def recurse(self, primes, max_times, index, value, divisors):
        if divisors >= self.min_presents:
            if value < self.global_min:
                self.global_min = value
            return
        if index >= len(primes):
            return
        for exp, div in enumerate(max_times[index]):
            self.recurse(primes, max_times, index + 1, value * primes[index]**exp, divisors * div)

    def solve2(self):
        # Assumption: value is divisible by 6, because that'll result in
        # 33 out of 50 numbers visited by elves.
        for n in range(0, self.min_presents // 11, 6):
            result = 0
            for d in range(1, 51):
                if n % d == 0:
                    result += n // d
            if result * 11 >= self.min_presents:
                return str(n)

r = runner()
r.run()
