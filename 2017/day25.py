import adventofcode
import re
from collections import defaultdict

class state_action:
    def __init__(self):
        self.write = 0
        self.move = 0
        self.next_state = None

class state:
    def __init__(self, name):
        self.name = name
        self.on = [state_action(), state_action()]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.start_state = None
        self.steps = 0
        self.states = dict()

    def input_line(self, line):
        m = re.match(r'Begin in state ([A-Z]).', line)
        if m:
            self.start_state = m.group(1)
            return
        m = re.match(r'Perform a diagnostic checksum after (\d+) steps.', line)
        if m:
            self.steps = int(m.group(1))
            return
        m = re.match(r'In state ([A-Z]):', line)
        if m:
            s = m.group(1)
            self.states[s] = self.current_state = state(s)
            return
        m = re.match(r'  If the current value is (\d):', line)
        if m:
            self.current_action = self.current_state.on[int(m.group(1))]
            return
        m = re.match(r'    - Write the value (\d).', line)
        if m:
            self.current_action.value = int(m.group(1))
            return
        m = re.match(r'    - Move one slot to the (right|left).', line)
        if m:
            self.current_action.move = -1 if m.group(1) == 'left' else +1
            return
        m = re.match(r'    - Continue with state ([A-Z]).', line)
        if m:
            self.current_action.next_state = m.group(1)
            return

    def solve1(self):
        tape = defaultdict(int)
        cursor = 0
        state = self.states[self.start_state]
        for n in range(self.steps):
            action = state.on[tape[cursor]]
            tape[cursor] = action.value
            cursor += action.move
            state = self.states[action.next_state]
        return sum(tape.values())

    def solve2(self):
        pass

r = runner()
r.run()
