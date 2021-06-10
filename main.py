class IncoherenceError:
    def __init__(self, conflict, container):
        self.Message = 'IncoherenceError: cannot define values for'
        self.Container = container
        self.Conflict = conflict

    def formatter(self, items):
        return f"""'{", '".join([str(item) + "'" for item in items])}"""

    def __repr__(self):
        return f"""{self.Message} {self.formatter(self.Conflict)} through {self.formatter(self.Container)} due to logical rules' contradiction.\n"""
    
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
    def __init__(self, proposition, verbose = False):
        self.Symbol = ''
        self.Propositions = (proposition,)
        self.Verbose = verbose

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                self.Value == True: (True,)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                self.Propositions[0].getValue() == True: True,
                self.Propositions[0].getValue() == False: False
            }
            self.setConnectiveValue()

    def setPropositionValue(self):
        try:
            for index in range(len(self.Propositions)):
                if self.Propositions[index].getValue() != self.Structure[True][index]:
                    old = self.Propositions[index].getValue()
                    self.Propositions[index].setValue(self.Structure[True][index])
                    if self.Verbose:
                        print(f' Proposition [{self.Propositions[index]}] '.center(80, '-') + '\n')
                        print(f'Changed value for proposition:\t{self.Propositions[index]}')
                        print(f'due to statements(s):'.rjust(30) + f'\t{self.__repr__()}\n')
                        print(f'Previous value:\t{old}')
                        print(f'New value:\t{self.Propositions[index].getValue()}\n')
        except KeyError:
            print(IncoherenceError(self.Propositions, [self.__repr__()]))

    def setConnectiveValue(self):
        try:
            if self.getValue() != self.Structure[True]:
                old = self.getValue()
                self.Value = self.Structure[True]
                if self.Verbose:
                    print(f' Connective [{self.__repr__()}] '.center(80, '-') + '\n')
                    print(f'Changed value for connective:\t{self.__repr__()}') 
                    print(f'due to statement(s):'.rjust(29) + f'\t{str(self.Propositions)[1:-1]}\n')
                    print(f'Previous value:\t{old}')
                    print(f'New value:\t{self.getValue()}\n')
        except KeyError:
            print(IncoherenceError([self.__repr__()], self.Propositions))

    def undefinedPropositionValue(self):
        return True if 'Undefined' in [proposition.getValue() for proposition in self.Propositions] else False

    def __repr__(self):
        return f'({self.Symbol}{str(self.Propositions)[1:-2]})'

class Not(Symbol):
    def __init__(self, proposition, verbose = False):
        self.Symbol = '¬'
        self.Propositions = (proposition,)
        self.Verbose = verbose

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                self.Value == True: (False,)
            }
            self.setPropositionValue()
        else:
            self.Structure = {
                self.Proposition[0].getValue() == True: (False,),
                self.Proposition[0].getValue() == False: (True,)
            }
            self.setConnectiveValue()

class And(Symbol):
    def __init__(self, proposition_1, proposition_2, verbose = False):
        self.Symbol = '^'
        self.Propositions = (proposition_1, proposition_2)
        self.Verbose = verbose

        self.Value = True
        if self.undefinedPropositionValue():
            self.Structure = {
                (self.getValue(), self.Propositions[0].getValue()) == (True, True): (True, True),
                (self.getValue(), self.Propositions[1].getValue()) == (True, True): (True, True)
            }
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
    def __init__(self, proposition_1, proposition_2, verbose = False):
        self.Symbol = 'v'
        self.Propositions = (proposition_1, proposition_2)
        self.Verbose = verbose

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
    def __init__(self, proposition_1, proposition_2, verbose = False):
        self.Symbol = '⟶'
        self.Propositions = (proposition_1, proposition_2)
        self.Verbose = verbose

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
    def __init__(self, proposition_1, proposition_2, verbose = False):
        self.Symbol = '⟷'
        self.Propositions = (proposition_1, proposition_2)
        self.Verbose = verbose

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

def summary(*statements):
    t1, t2, t3 = 'ID:', 'Value:', 'Element:'
    idlen, vallen, ellen = 5, 15, 60
    title = t1 + (idlen - len(t1)) * ' ' + t2 + (vallen - len(t2)) * ' ' + t3 + (ellen - len(t3)) * ' '
    print('-' * 80)
    print(title)
    print('-' * 80)
    for index in range(len(statements)):
        r1 = str(index)
        r2 = str(statements[index].getValue())
        r3 = str(statements[index])
        row = r1 + (idlen - len(r1)) * ' ' + r2 + (vallen - len(r2)) * ' ' + r3 + (ellen - len(r3)) * ' '
        print(row)
