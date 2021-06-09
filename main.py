# Annotation 1: connectives and propositions are, originally, dynamic elements,
#   since their values can be mutated on declaration, yet from that point they
#   are static, since they have a defined value unless re-evaluated.

# Annotation 2: do propositions and connectives have equal value relations?
#   (does one have preference over the other or not?)

class Proposition:
    """Contains basic data for propositions."""
    def __init__(self, description: str):
        self.Description = description
        self.Value = 'Undefined'

    def __repr__(self):
        return f'{self.Description}'
    
    # Setter and getter methods:

    def getSelfValue(self):
        return self.Value

    def setSelfValue(self, value):
        self.Value = value

# Main connective class:

class Connective:
    """Defines standard operational behavior for all connectives.

    Connectives' values must be 'True' by default due to the fact that they are
    used to define propositions' values, and therefore require a boolean
    evaluation instead of an 'Undefined' statement.

    The structure of each class matches the following pattern:

        1. Proposition and verbose definition.
        2. Symbol definition.
        3. Relations structure definition and evaluation.

    """
    def __init__(self, verbose: bool = False):
        self.Symbol = ''
        self.Value = True
        self.Verbose = verbose

    # Setter and getter methods:

    def getSelfValue(self):
        return self.Value

    def setSelfValue(self, value):
        self.Value = value

# Main connective class subdivisions:

class UnaryConnective(Connective):
    """Defines specific behavior for single proposition connectives."""
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(verbose)
        self.Proposition = proposition
        
    def __repr__(self):
        return f'{self.Symbol}{self.Proposition}'
    
    # Setter and getter methods:

    def getPropValue(self):
        return self.Proposition.getSelfValue()

    def setPropValue(self, value):
        self.Proposition.setSelfValue(value)

    def setValues(self, values):
        self.setSelfValue(values[0])
        self.setPropValue(values[1])

    # Incoherence check:

    def check(self):
        if 'Undefined' in [self.getSelfValue(), self.getPropValue()]:
            print(f"[Logic] Warning: '{self.__repr__()}' with value {self.getSelfValue()} and propositions ('{self.Proposition}', {self.getPropValue()}) has undefined values.")

class BinaryConnective(Connective):
    """Defines specific behavior for double proposition connectives."""
    def __init__(self, proposition_1: Proposition, proposition_2: Proposition, verbose: bool = False):
        super().__init__(verbose)
        self.Propositions = (proposition_1, proposition_2)

    def __repr__(self):
        return f'{self.Propositions[0]} {self.Symbol} {self.Propositions[1]}'

    # Setter and getter methods:

    def getPropValue(self):
        return (self.Propositions[0].getSelfValue(), self.Propositions[1].getSelfValue())

    def setPropValue(self, values):
        for index in range(len(self.Propositions)):
            self.Propositions[index].setSelfValue(values[index])

    def setValues(self, values):
        self.setSelfValue(values[0])
        self.setPropValue(values[1])

    # Incoherence check:

    def check(self):
        if 'Undefined' == self.getSelfValue() or 'Undefined' in self.getPropValue():
            undefined = []
            for index in range(len(self.getPropValue())):
                undefined.append(self.Propositions[index]) if self.getPropValue()[index] == 'Undefined' else None
            print(f"Warning: '{self.__repr__()}' ({self.getSelfValue()}) has undefined values in proposition(s): {undefined[0] if len(undefined) == 1 else str(tuple(undefined))[1:-1]}.")

# Unary connectives:

class Yes(UnaryConnective):
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(proposition, verbose)

        self.Structure = {
            (self.getSelfValue(), self.getPropValue()) == (True, True):                 (True, True),
            (self.getSelfValue(), self.getPropValue()) == (True, False):                (True, False),
            (self.getSelfValue(), self.getPropValue()) == (True, 'Undefined'):          (True, True),       # Special Case 1

            (self.getSelfValue(), self.getPropValue()) == (False, True):                (False, False),
            (self.getSelfValue(), self.getPropValue()) == (False, False):               (False, True),
            (self.getSelfValue(), self.getPropValue()) == (False, 'Undefined'):         (False, False),     # Special Case 2

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', True):          (True, True),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', False):         (False, False),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', 'Undefined'):   ('Undefined', 'Undefined')
        }
        self.setValues(self.Structure[True])
        self.check()

class Not(UnaryConnective):
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(proposition, verbose)
        self.Symbol = '¬'

        self.Structure = {
            (self.getSelfValue(), self.getPropValue()) == (True, True):                 (True, False),
            (self.getSelfValue(), self.getPropValue()) == (True, False):                (True, True),
            (self.getSelfValue(), self.getPropValue()) == (True, 'Undefined'):          (True, False),      # Special Case 3

            (self.getSelfValue(), self.getPropValue()) == (False, True):                (False, True),
            (self.getSelfValue(), self.getPropValue()) == (False, False):               (False, False),
            (self.getSelfValue(), self.getPropValue()) == (False, 'Undefined'):         (False, True),      # Special Case 4

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', True):          (False, True),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', False):         (True, False),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', 'Undefined'):   ('Undefined', 'Undefined')
        }
        self.setValues(self.Structure[True])
        self.check()
        
# Binary connectives:

class And(BinaryConnective):
    def __init__(self, proposition_1, proposition_2, verbose: bool = False):
        super().__init__(proposition_1, proposition_2, verbose)
        self.Propositions = (proposition_1, proposition_2)
        self.Symbol = '^'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, (True, True)):                         (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (True, False)):                        (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, True)):                        (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, False)):                       (False, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, True)):                        (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (True, False)):                       (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, True)):                       (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, False)):                      (False, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, False)):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, True)):                 (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, False)):                (False, (False, False)),

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (True, (True, 'Undefined')):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, 'Undefined')):                 (False, (False, 'Undefined')),          # Special Case 1
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', False)):                 (False, ('Undefined', False)),          # Special Case 2

            (self.getSelfValue(), self.getPropValue()) == (False, (True, 'Undefined')):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, 'Undefined')):                (False, (False, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', True)):                 (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', False)):                (False, (False, False)),
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, 'Undefined')):           ('Undefined', (True, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, 'Undefined')):          (False, (False, 'Undefined')),          # Special Case 3
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', True)):           ('Undefined', ('Undefined', True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', False)):          (False, ('Undefined', False)),          # Special Case 4

            # Standard 'else':

            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', 'Undefined')):           (True, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', 'Undefined')):          (False, ('Undefined', 'Undefined')),            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', 'Undefined')):    ('Undefined', ('Undefined', 'Undefined'))
        }
        self.setValues(self.Structure[True])
        self.check()

class Or(BinaryConnective):
    def __init__(self, proposition_1, proposition_2, verbose = False):
        super().__init__(proposition_1, proposition_2, verbose)
        self.Symbol = 'v'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, (True, True)):                         (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (True, False)):                        (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, True)):                        (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, False)):                       (False, (False, False)),
            
            (self.getSelfValue(), self.getPropValue()) == (False, (True, True)):                        (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (True, False)):                       (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, True)):                       (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, False)):                      (False, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, False)):                 (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, True)):                 (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, False)):                (False, (False, False)),

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (True, (True, 'Undefined')):                  (True, (True, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, 'Undefined')):                 (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', True)):                  (True, ('Undefined', True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', False)):                 (True, (True, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, 'Undefined')):                 (True, (True, 'Undefined')),            # Special Case 1
            (self.getSelfValue(), self.getPropValue()) == (False, (False, 'Undefined')):                (False, (False, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', True)):                 (True, ('Undefined', True)),            # Special Case 2
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', False)):                (False, ('Undefined', False)),
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', True)):           (True, ('Undefined', True)),            # Special Case 3
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', False)):          ('Undefined', ('Undefined', False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, 'Undefined')):           (True, (True, 'Undefined')),            # Special Case 4
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, 'Undefined')):          ('Undefined', (False, 'Undefined')),

            # Standard 'else':
            
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', 'Undefined')):           (True, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', 'Undefined')):          (False, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', 'Undefined')):    ('Undefined', ('Undefined', 'Undefined'))
        }
        self.setValues(self.Structure[True])
        self.check()

class XOr(BinaryConnective):
    def __init__(self, proposition_1, proposition_2, verbose = False):
        super().__init__(proposition_1, proposition_2, verbose)
        self.Symbol = 'xv'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, (True, True)):                         (False, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (True, False)):                        (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, True)):                        (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, False)):                       (False, (False, False)),
            
            (self.getSelfValue(), self.getPropValue()) == (False, (True, True)):                        (False, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (True, False)):                       (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, True)):                       (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, False)):                      (False, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, True)):                  (False, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, False)):                 (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, True)):                 (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, False)):                (False, (False, False)),

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (True, (True, 'Undefined')):                  (True, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, 'Undefined')):                 (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', True)):                  (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', False)):                 (True, (True, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, 'Undefined')):                 (False, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, 'Undefined')):                (False, (False, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', True)):                 (False, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', False)):                (False, (False, False)),
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', True)):           ('Undefined', ('Undefined', True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', False)):          ('Undefined', ('Undefined', False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, 'Undefined')):           ('Undefined', (True, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, 'Undefined')):          ('Undefined', (False, 'Undefined')),

            # Standard 'else':
            
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', 'Undefined')):           (True, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', 'Undefined')):          (False, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', 'Undefined')):    ('Undefined', ('Undefined', 'Undefined'))
        }
        self.setValues(self.Structure[True])

class Implicative(BinaryConnective):
    def __init__(self, proposition_1, proposition_2, verbose = False):
        super().__init__(proposition_1, proposition_2, verbose)
        self.Propositions = (proposition_1, proposition_2)
        self.Symbol = '⟶'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, (True, True)):                         (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (True, False)):                        (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, True)):                        (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, False)):                       (True, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, True)):                        (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (True, False)):                       (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, True)):                       (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, False)):                      (True, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, False)):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, True)):                 (True, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, False)):                (True, (False, False)),

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (True, (True, 'Undefined')):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, 'Undefined')):                 (True, (False, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', False)):                 ('Undefined', ('Undefined', False)),    # Special Case 1

            (self.getSelfValue(), self.getPropValue()) == (False, (True, 'Undefined')):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, 'Undefined')):                (True, (False, 'Undefined')),           # Special Case 2
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', True)):                 (True, ('Undefined', True)),            # Special Case 3
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', False)):                (False, (True, False)),
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, 'Undefined')):           ('Undefined', (True, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, 'Undefined')):          (True, (False, 'Undefined')),           # Special Case 4
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', True)):           ('Undefined', ('Undefined', True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', False)):          (False, ('Undefined', False)),          # Special Case 5

            # Standard 'else':

            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', 'Undefined')):           (True, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', 'Undefined')):          (False, ('Undefined', 'Undefined')),            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', 'Undefined')):    ('Undefined', ('Undefined', 'Undefined'))
        }
        self.setValues(self.Structure[True])

class BiImplicative(And):
    def __init__(self, proposition_1, proposition_2, verbose = False):
        super().__init__(proposition_1, proposition_2, verbose)
        self.Symbol = '⟷'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, (True, True)):                         (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (True, False)):                        (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, True)):                        (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, False)):                       (True, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, True)):                        (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (True, False)):                       (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, True)):                       (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, False)):                      (True, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, False)):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, True)):                 (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, False)):                (True, (False, False)),

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (True, (True, 'Undefined')):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, (False, 'Undefined')):                 (True, (False, False)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', True)):                  (True, (True, True)),
            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', False)):                 (True, (False, False)),

            (self.getSelfValue(), self.getPropValue()) == (False, (True, 'Undefined')):                 (False, (True, False)),
            (self.getSelfValue(), self.getPropValue()) == (False, (False, 'Undefined')):                (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', True)):                 (False, (False, True)),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', False)):                (False, (True, False)),
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (True, 'Undefined')):           ('Undefined', (True, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', (False, 'Undefined')):          ('Undefined', (False, 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', True)):           ('Undefined', ('Undefined', True)),
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', False)):          ('Undefined', ('Undefined', False)),

            # Standard 'else':

            (self.getSelfValue(), self.getPropValue()) == (True, ('Undefined', 'Undefined')):           (True, ('Undefined', 'Undefined')),
            (self.getSelfValue(), self.getPropValue()) == (False, ('Undefined', 'Undefined')):          (False, ('Undefined', 'Undefined')),            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', ('Undefined', 'Undefined')):    ('Undefined', ('Undefined', 'Undefined'))
        }
        self.setValues(self.Structure[True])
