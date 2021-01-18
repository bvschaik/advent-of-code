import adventofcode
from collections import defaultdict, deque

class duet_program:
    def __init__(self, program, is_duet = False, p_init = 0):
        self.program = program
        self.registers = defaultdict(int)
        self.ip = 0
        self.execute = {
            'set': self.set,
            'add': self.add,
            'mul': self.mul,
            'mod': self.mod,
            'jgz': self.jgz
        }
        if is_duet:
            self.name = is_duet
            self.execute['snd'] = self.send
            self.execute['rcv'] = self.receive
            self.input_queue = deque()
            self.num_sends = 0
            self.registers['p'] = p_init
        else:
            self.execute['snd'] = self.sound
            self.execute['rcv'] = self.recover

    def set(self, x, y):
        self.registers[x] = self.get_value(y)
        self.ip += 1

    def add(self, x, y):
        self.registers[x] += self.get_value(y)
        self.ip += 1

    def mul(self, x, y):
        self.registers[x] *= self.get_value(y)
        self.ip += 1

    def mod(self, x, y):
        self.registers[x] %= self.get_value(y)
        self.ip += 1

    def jgz(self, x, y):
        if self.get_value(x) > 0:
            self.ip += self.get_value(y)
        else:
            self.ip += 1

    def sound(self, x):
        self.last_sound = self.get_value(x)
        self.ip += 1

    def recover(self, x):
        if self.get_value(x) != 0:
            self.stop = True
        self.ip += 1

    def send(self, x):
        self.output_queue.append(self.get_value(x))
        self.ip += 1
        self.num_sends += 1

    def receive(self, x):
        if self.input_queue:
            self.registers[x] = self.input_queue.popleft()
            self.ip += 1
        else:
            self.blocked = True

    def get_value(self, operand):
        if operand >= 'a' and operand <= 'z':
            return self.registers[operand]
        else:
            return int(operand)

    def run(self):
        self.stop = False
        self.last_sound = 0
        max_ip = len(self.program)
        while self.ip >= 0 and self.ip < max_ip and not self.stop:
            line = self.program[self.ip]
            if len(line) == 2:
                self.execute[line[0]](line[1])
            else:
                self.execute[line[0]](line[1], line[2])
        return self.last_sound

    def run_duet(self):
        self.blocked = False
        max_ip = len(self.program)
        while self.ip >= 0 and self.ip < max_ip and not self.blocked:
            line = self.program[self.ip]
            if len(line) == 2:
                self.execute[line[0]](line[1])
            else:
                self.execute[line[0]](line[1], line[2])
        return self.blocked

    def is_deadlock(self):
        return self.blocked and not self.input_queue

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(18)

    def reset(self):
        self.program = []

    def input_line(self, line):
        self.program.append(line.split())

    def solve1(self):
        p = duet_program(self.program)
        return str(p.run())

    def solve2(self):
        a = duet_program(self.program, 'a', 0)
        b = duet_program(self.program, 'b', 1)
        a.output_queue = b.input_queue
        b.output_queue = a.input_queue

        while a.run_duet() and b.run_duet():
            if a.is_deadlock() and b.is_deadlock():
                break
        return str(b.num_sends)

r = runner()

r.test('Sample', [
    'set a 1',
    'add a 2',
    'mul a a',
    'mod a 5',
    'snd a',
    'set a 0',
    'rcv a',
    'jgz a -1',
    'set a 1',
    'jgz a -2',
], '4')

r.run()
