import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.numbers = []

    def input_line(self, line):
        self.numbers.append(int(line))

    def solve1(self):
        adapters = sorted(self.numbers)
        phone_jolts = adapters[len(adapters) - 1] + 3
        adapters.append(phone_jolts)
        step1 = 0
        step3 = 0
        prev = 0
        for i in adapters:
            diff = i - prev
            if diff == 1:
                step1 += 1
            elif diff == 3:
                step3 += 1
            prev = i
        return str(step1 * step3)

    def solve2(self):
        adapters = sorted(self.numbers)
        phone_jolts = adapters[len(adapters) - 1] + 3
        adapters.append(phone_jolts)
        paths = dict()
        paths[0] = 1
        for i in adapters:
            paths[i] = 0
            for step in [1, 2, 3]:
                if i - step in paths:
                    paths[i] += paths[i - step]
        return str(paths[phone_jolts])

r = runner()

r.test('Sample 1', [
    '28',
    '33',
    '18',
    '42',
    '31',
    '14',
    '46',
    '20',
    '48',
    '47',
    '24',
    '23',
    '49',
    '45',
    '19',
    '38',
    '39',
    '11',
    '1',
    '32',
    '25',
    '35',
    '8',
    '17',
    '7',
    '9',
    '4',
    '2',
    '34',
    '10',
    '3',
], '220', '19208')

r.run()
