import re
from runner import runner

class log_entry:
    GUARD = 0
    SLEEP = 1
    WAKE = 2

    def __init__(self, line):
        m = re.match(r"^\[(.* (\d+):(\d+))\] (.*)$", line)
        self.timestamp = m.group(1)
        self.hour = int(m.group(2))
        self.minute = int(m.group(3))
        self.desc = m.group(4)
        if self.desc == 'falls asleep':
            self.type = log_entry.SLEEP
        elif self.desc == 'wakes up':
            self.type = log_entry.WAKE
        else:
            self.type = log_entry.GUARD
            self.guard = int(re.match(r"Guard #(\d+)", self.desc).group(1))

    def __repr__(self):
        return str.format("log_entry(timestamp=%s, hour=%d, minute=%d, desc=%s)" % (self.timestamp, self.hour, self.minute, self.desc))

class guard_data:
    def __init__(self, id):
        self.id = id
        self.total_minutes_asleep = 0
        self.sleeping_minutes = [0] * 60
    
    def record_sleep(self, start, end):
        self.total_minutes_asleep += end - start
        for minute in range(start, end):
            self.sleeping_minutes[minute] += 1
    
    def max_sleeping_minute(self):
        return max(enumerate(self.sleeping_minutes), key = lambda x: x[1])

class day04(runner):
    def __init__(self):
        self.inputs = []

    def day(self):
        return 4
    
    def input(self, line):
        self.inputs.append(log_entry(line))

    def solve1(self):
        entries = sorted(self.inputs, key = lambda x: x.timestamp)

        guards = dict()
        data = None
        sleep_time = None
        for entry in entries:
            if entry.type == log_entry.GUARD:
                if sleep_time is not None:
                    raise AssertionError("Guard change while previous guard is asleep!")
                if entry.guard not in guards:
                    guards[entry.guard] = guard_data(entry.guard)
                data = guards[entry.guard]
            elif entry.type == log_entry.SLEEP and entry.hour == 0:
                sleep_time = entry.minute
            elif entry.type == log_entry.WAKE:
                if sleep_time is None:
                    raise AssertionError("Waking up before sleeping?")
                end_time = entry.minute if entry.hour == 0 else 59
                data.record_sleep(sleep_time, end_time)
                sleep_time = None

        sleepy_guard = max(guards.values(), key = lambda x: x.total_minutes_asleep)
        sleepy_minute = sleepy_guard.max_sleeping_minute()[0]
        return str(sleepy_guard.id * sleepy_minute)

    def solve2(self):
        entries = sorted(self.inputs, key = lambda x: x.timestamp)

        guards = dict()
        data = None
        sleep_time = None
        for entry in entries:
            if entry.type == log_entry.GUARD:
                if sleep_time is not None:
                    raise AssertionError("Guard change while previous guard is asleep!")
                if entry.guard not in guards:
                    guards[entry.guard] = guard_data(entry.guard)
                data = guards[entry.guard]
            elif entry.type == log_entry.SLEEP and entry.hour == 0:
                sleep_time = entry.minute
            elif entry.type == log_entry.WAKE:
                if sleep_time is None:
                    raise AssertionError("Waking up before sleeping?")
                end_time = entry.minute if entry.hour == 0 else 59
                data.record_sleep(sleep_time, end_time)
                sleep_time = None

        sleepy_guard = max(guards.values(), key = lambda x: x.max_sleeping_minute()[1])
        return str(sleepy_guard.id * sleepy_guard.max_sleeping_minute()[0])

day04().test('Sample problem', [
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up'
], '240', '4455')

day04().solve()
