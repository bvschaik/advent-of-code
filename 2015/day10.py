import adventofcode

# The "Look and Say" sequence has an interesting notion of atomic "elements" which decay into
# one or more other atomic elements on the next step in the sequence. Since they're shorter
# to keep in memory, representing strings with elements instead will significantly speed up
# calculating the next number.

periodic_elements = {
    'H': '22',
    'He': '13112221133211322112211213322112',
    'Li': '312211322212221121123222112',
    'Be': '111312211312113221133211322112211213322112',
    'B': '1321132122211322212221121123222112',
    'C': '3113112211322112211213322112',
    'N': '111312212221121123222112',
    'O': '132112211213322112',
    'F': '31121123222112',
    'Ne': '111213322112',
    'Na': '123222112',
    'Mg': '3113322112',
    'Al': '1113222112',
    'Si': '1322112',
    'P': '311311222112',
    'S': '1113122112',
    'Cl': '132112',
    'Ar': '3112',
    'K': '1112',
    'Ca': '12',
    'Sc': '3113112221133112',
    'Ti': '11131221131112',
    'V': '13211312',
    'Cr': '31132',
    'Mn': '111311222112',
    'Fe': '13122112',
    'Co': '32112',
    'Ni': '11133112',
    'Cu': '131112',
    'Zn': '312',
    'Ga': '13221133122211332',
    'Ge': '31131122211311122113222',
    'As': '11131221131211322113322112',
    'Se': '13211321222113222112',
    'Br': '3113112211322112',
    'Kr': '11131221222112',
    'Rb': '1321122112',
    'Sr': '3112112',
    'Y': '1112133',
    'Zr': '12322211331222113112211',
    'Nb': '1113122113322113111221131221',
    'Mo': '13211322211312113211',
    'Tc': '311322113212221',
    'Ru': '132211331222113112211',
    'Rh': '311311222113111221131221',
    'Pd': '111312211312113211',
    'Ag': '132113212221',
    'Cd': '3113112211',
    'In': '11131221',
    'Sn': '13211',
    'Sb': '3112221',
    'Te': '1322113312211',
    'I': '311311222113111221',
    'Xe': '11131221131211',
    'Cs': '13211321',
    'Ba': '311311',
    'La': '11131',
    'Ce': '1321133112',
    'Pr': '31131112',
    'Nd': '111312',
    'Pm': '132',
    'Sm': '311332',
    'Eu': '1113222',
    'Gd': '13221133112',
    'Tb': '3113112221131112',
    'Dy': '111312211312',
    'Ho': '1321132',
    'Er': '311311222',
    'Tm': '11131221133112',
    'Yb': '1321131112',
    'Lu': '311312',
    'Hf': '11132',
    'Ta': '13112221133211322112211213322113',
    'W': '312211322212221121123222113',
    'Re': '111312211312113221133211322112211213322113',
    'Os': '1321132122211322212221121123222113',
    'Ir': '3113112211322112211213322113',
    'Pt': '111312212221121123222113',
    'Au': '132112211213322113',
    'Hg': '31121123222113',
    'Tl': '111213322113',
    'Pb': '123222113',
    'Bi': '3113322113',
    'Po': '1113222113',
    'At': '1322113',
    'Rn': '311311222113',
    'Fr': '1113122113',
    'Ra': '132113',
    'Ac': '3113',
    'Th': '1113',
    'Pa': '13',
    'U': '3',
}

periodic_decay = {
    'H': ['H'],
    'He': ['Hf', 'Pa', 'H', 'Ca', 'Li'],
    'Li': ['He'],
    'Be': ['Ge', 'Ca', 'Li'],
    'B': ['Be'],
    'C': ['B'],
    'N': ['C'],
    'O': ['N'],
    'F': ['O'],
    'Ne': ['F'],
    'Na': ['Ne'],
    'Mg': ['Pm', 'Na'],
    'Al': ['Mg'],
    'Si': ['Al'],
    'P': ['Ho', 'Si'],
    'S': ['P'],
    'Cl': ['S'],
    'Ar': ['Cl'],
    'K': ['Ar'],
    'Ca': ['K'],
    'Sc': ['Ho', 'Pa', 'H', 'Ca', 'Co'],
    'Ti': ['Sc'],
    'V': ['Ti'],
    'Cr': ['V'],
    'Mn': ['Cr', 'Si'],
    'Fe': ['Mn'],
    'Co': ['Fe'],
    'Ni': ['Zn', 'Co'],
    'Cu': ['Ni'],
    'Zn': ['Cu'],
    'Ga': ['Eu', 'Ca', 'Ac', 'H', 'Ca', 'Zn'],
    'Ge': ['Ho', 'Ga'],
    'As': ['Ge', 'Na'],
    'Se': ['As'],
    'Br': ['Se'],
    'Kr': ['Br'],
    'Rb': ['Kr'],
    'Sr': ['Rb'],
    'Y': ['Sr', 'U'],
    'Zr': ['Y', 'H', 'Ca', 'Tc'],
    'Nb': ['Er', 'Zr'],
    'Mo': ['Nb'],
    'Tc': ['Mo'],
    'Ru': ['Eu', 'Ca', 'Tc'],
    'Rh': ['Ho', 'Ru'],
    'Pd': ['Rh'],
    'Ag': ['Pd'],
    'Cd': ['Ag'],
    'In': ['Cd'],
    'Sn': ['In'],
    'Sb': ['Pm', 'Sn'],
    'Te': ['Eu', 'Ca', 'Sb'],
    'I': ['Ho', 'Te'],
    'Xe': ['I'],
    'Cs': ['Xe'],
    'Ba': ['Cs'],
    'La': ['Ba'],
    'Ce': ['La', 'H', 'Ca', 'Co'],
    'Pr': ['Ce'],
    'Nd': ['Pr'],
    'Pm': ['Nd'],
    'Sm': ['Pm', 'Ca', 'Zn'],
    'Eu': ['Sm'],
    'Gd': ['Eu', 'Ca', 'Co'],
    'Tb': ['Ho', 'Gd'],
    'Dy': ['Tb'],
    'Ho': ['Dy'],
    'Er': ['Ho', 'Pm'],
    'Tm': ['Er', 'Ca', 'Co'],
    'Yb': ['Tm'],
    'Lu': ['Yb'],
    'Hf': ['Lu'],
    'Ta': ['Hf', 'Pa', 'H', 'Ca', 'W'],
    'W': ['Ta'],
    'Re': ['Ge', 'Ca', 'W'],
    'Os': ['Re'],
    'Ir': ['Os'],
    'Pt': ['Ir'],
    'Au': ['Pt'],
    'Hg': ['Au'],
    'Tl': ['Hg'],
    'Pb': ['Tl'],
    'Bi': ['Pm', 'Pb'],
    'Po': ['Bi'],
    'At': ['Po'],
    'Rn': ['Ho', 'At'],
    'Fr': ['Rn'],
    'Ra': ['Fr'],
    'Ac': ['Ra'],
    'Th': ['Ac'],
    'Pa': ['Th'],
    'U': ['Pa'],
}

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.input = None

    def input_line(self, line):
        self.input_string = line
        self.input = list(map(int, line))

    def solve1(self):
        line = self.input
        for _ in range(40):
            line = self.say(line)
        return str(len(line))

    def say(self, line):
        prev = None
        times = 0
        result = []
        for n in line:
            if n == prev:
                times += 1
            else:
                if times > 0:
                    result.append(times)
                    result.append(prev)
                prev = n
                times = 1
        if times > 0:
            result.append(times)
            result.append(prev)
        return result

    def solve2(self):
        elements = None
        for e in periodic_elements:
            if periodic_elements[e] == self.input_string:
                elements = [e]
                break
        if not elements:
            print("Start is not an element")
            return
        for n in range(50):
            elements = self.say_periodic(elements)
        length = 0
        for e in elements:
            length += len(periodic_elements[e])
        return str(length)

    def say_periodic(self, elements):
        result = []
        for e in elements:
            result.extend(periodic_decay[e])
        return result

r = runner()
r.run()
