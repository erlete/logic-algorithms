class Proposition:
    def __init__(self, name):
        self.Name = name
        self.Value = 'Undefined'

    def setValue(self, value):
        self.Value = value if self.Value == 'Undefined' else self.Value

    def getValue(self):
        try:
            return self.Value
        except AttributeError:
            return 'Undefined'

    def __repr__(self):
        return f'{self.Name}'

class Symbol(Proposition):
    def __init__(self, proposition):
        self.Symbol = ''
        self.Propositions = (proposition,)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                self.Value == True: (True,)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                self.Proposition[0].getValue() == True: True,
                self.Proposition[0].getValue() == False: False
            }
            self.setConnectiveValue()

    def setPropositionValue(self):
        for index in range(len(self.Propositions)):
            print(f"Changed value for proposition:\t{self.Propositions[index]}\n\tdue to connective:\t{self.__repr__()}\n")
            print(f'Previous value:\t{self.Propositions[index].getValue()}')
            self.Propositions[index].setValue(self.Structure[True][index])
            print(f'Actual value:\t{self.Propositions[index].getValue()}\n')

    def setConnectiveValue(self):
        print(f"Changed value for connective:\t{self.__repr__()}\n\tdue to propositions:\t{self.Propositions[0]}: {self.Propositions[0].getValue()}\n\tand\t\t\t{self.Propositions[1]}: {self.Propositions[1].getValue()}\n")
        print(f'Previous value:\t{self.getValue()}')
        self.Value = self.Structure[True]
        print(f'Actual value:\t{self.getValue()}\n')

    def undefinedPropositionValue(self):
        return True if 'Undefined' in [proposition.getValue() for proposition in self.Propositions] else False

    def __repr__(self):
        return f'{self.Symbol}{str(self.Propositions)[1:-2]}'

class Not(Symbol):
    def __init__(self, proposition):
        self.Symbol = '¬'
        self.Propositions = (proposition,)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                self.Value == True: (False,)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                self.Proposition[0].getValue() == True: False,
                self.Proposition[0].getValue() == False: True
            }
            self.setConnectiveValue()

class And(Symbol):
    def __init__(self, proposition_1, proposition_2):
        self.Symbol = '^'
        self.Propositions = (proposition_1, proposition_2)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                (self.getValue(), self.Propositions[0].getValue()) == (True, True): (True, True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, True): (True, True)
            }
            print(self.Structure)
            self.setPropositionValue()
        else:
            self.Structure = {
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, True): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, False): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, True): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, False): False
            }
            self.setConnectiveValue()

    def __repr__(self):
        return f'({self.Propositions[0]} {self.Symbol} {self.Propositions[1]})'

class Or(And):
    def __init__(self, proposition_1, proposition_2):
        self.Symbol = 'v'
        self.Propositions = (proposition_1, proposition_2)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                (self.getValue(), self.Propositions[0].getValue()) == (True, True): (True, False),
                (self.getValue(), self.Propositions[0].getValue()) == (True, False): (False, True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, True): (False, True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, False): (True, False)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, True): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, False): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, True): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, False): False
            }
            self.setConnectiveValue()

class Implicative(And):
    def __init__(self, proposition_1, proposition_2):
        self.Symbol = '⟶'
        self.Propositions = (proposition_1, proposition_2)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                (self.getValue(), self.Propositions[0].getValue()) == (True, True): (True, True),
                (self.getValue(), self.Propositions[0].getValue()) == (True, False): (False, 'Undefined'),
                (self.getValue(), self.Propositions[1].getValue()) == (True, True): ('Undefined', True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, False): (False, False)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, True): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, False): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, True): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, False): True
            }
            self.setConnectiveValue()

class BiImplicative(And):
    def __init__(self, proposition_1, proposition_2):
        self.Symbol = '⟷'
        self.Propositions = (proposition_1, proposition_2)

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                (self.getValue(), self.Propositions[0].getValue()) == (True, True): (True, True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, False): (False, False)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, True): True,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (True, False): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, True): False,
                (self.Propositions[0].getValue(), self.Propositions[1].getValue()) == (False, False): True
            }
            self.setConnectiveValue()

# Proposition generation (null values):
p = Proposition('rains')
q = Proposition('coat')
r = Proposition('umbrella')

print('-Basic proposition evaluation' + '-' * 51 + '\n')

print('# Evaluating s1\n')
s1 = Symbol(q)

print('## Evaluating s2\n')
s2 = Not(r)

print('-And + Implicative evaluation' + '-' * 51 + '\n')

print('### Evaluating s3\n')
s3 = And(q, r)

print('#### Evaluating s4\n')
s4 = BiImplicative(p, And(q, r))

print('-' * 80 + '\n')
