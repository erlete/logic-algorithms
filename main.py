class Proposition:
    """Contains basic data for propositions."""
    def __init__(self, description: str):
        self.Description = description
        self.Value = 'Undefined'

    def __repr__(self):
        return f'{self.Description}'

    def setSelfValue(self, value):
        """Sets the object's value."""
        self.Value = value

    def getSelfValue(self):
        """Returns the object's value."""
        return self.Value

# Main connective class:

class Connective:
    """Defines standard operational behavior for all connectives.

    The structure of each class matches the following pattern:

        1. Proposition and verbose definition.
        2. Symbol definition.
        3. Relations structure definition and evaluation.

    Connectives' values must be 'True' by default due to the fact that they are
    used to define propositions' values, and therefore require a boolean
    evaluation instead of an 'Undefined' statement.
    """
    def __init__(self, verbose: bool = False):
        self.Symbol = ''
        self.Value = True
        self.Verbose = verbose

    def setSelfValue(self, value):
        """Sets the object's value."""
        self.Value = value

    def getSelfValue(self):
        """Returns the object's value."""
        return self.Value

# Main connective class subdivisions:

class UnaryConnective(Connective):
    """Defines specific behavior for single proposition connectives."""
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(verbose)
        self.Proposition = proposition
        
    def __repr__(self):
        return f'[{self.Symbol}{self.Proposition}]'

    def setPropValue(self, value):
        """Sets the object's proposition value."""
        self.Proposition.setSelfValue(value)

    def setValues(self, values):
        """Call for both value setters of the given object."""
        self.setSelfValue(values[0])
        self.setPropValue(values[1])

    def getPropValue(self):
        """Returns the object's proposition value."""
        return self.Proposition.getSelfValue()

    def check(self):
        """Checks for 'Undefined' values inside of the connective."""
        if 'Undefined' in [self.getSelfValue(), self.getPropValue()]:
            print(f"[Logic] Warning: '{self.__repr__()}' with value {self.getSelfValue()} and propositions ('{self.Proposition}', {self.getPropValue()}) has undefined values.")

class BinaryConnective(Connective):
    """Defines specific behavior for double proposition connectives."""
    def __init__(self, proposition_1: Proposition, proposition_2: Proposition, verbose: bool = False):
        super().__init__(verbose)
        self.Propositions = (proposition_1, proposition_2)

    def __repr__(self):
        return f'[{self.Propositions[0]} {self.Symbol} {self.Propositions[1]}]'

    def setPropValue(self, values):
        """Sets the object's propositions' values."""
        for index in range(len(self.Propositions)):
            self.Propositions[index].setSelfValue(values[index])

    def setValues(self, values):
        """Call for both value setters of the given object."""
        self.setSelfValue(values[0])
        self.setPropValue(values[1])

    def getPropValue(self):
        """Returns the object's propositions' values."""
        return (self.Propositions[0].getSelfValue(), self.Propositions[1].getSelfValue())

    def check(self):
        """Checks for 'Undefined' values inside of the connective."""
        if 'Undefined' == self.getSelfValue() or 'Undefined' in self.getPropValue():
            undefined = []
            for index in range(len(self.getPropValue())):
                undefined.append(self.Propositions[index]) if self.getPropValue()[index] == 'Undefined' else None
            print(f"Warning: '{self.__repr__()}' ({self.getSelfValue()}) has undefined values in proposition(s): {undefined[0] if len(undefined) == 1 else str(tuple(undefined))[1:-1]}.")

# Unary connectives:

class Yes(UnaryConnective):
    """Truthy unary connective.

    If True, sets the value of the passed proposition to True, else inverts it.

    This connective is required as inverse of the 'Not' one.
    """
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(proposition, verbose)

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, True):                 (True, True),
            (self.getSelfValue(), self.getPropValue()) == (True, False):                (True, False),
            (self.getSelfValue(), self.getPropValue()) == (True, 'Undefined'):          (True, True),   # Class-Specific Case 1

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (False, True):                (False, False),
            (self.getSelfValue(), self.getPropValue()) == (False, False):               (False, True),
            (self.getSelfValue(), self.getPropValue()) == (False, 'Undefined'):         (False, False), # Class-Specific Case 2

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', True):          (True, True),   # Special Case 1
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', False):         (False, False), # Special Case 2

            # Standard 'else'

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', 'Undefined'):   ('Undefined', 'Undefined')
        }
        self.setValues(self.Structure[True])
        self.check()

class Not(UnaryConnective):
    """Falsy unary connective.

    If True, inverts the value of the passed proposition, else keeps it.
    """
    def __init__(self, proposition, verbose: bool = False):
        super().__init__(proposition, verbose)
        self.Symbol = '¬'

        self.Structure = {

            # Connective value definition:
            
            (self.getSelfValue(), self.getPropValue()) == (True, True):                 (True, False),
            (self.getSelfValue(), self.getPropValue()) == (True, False):                (True, True),
            (self.getSelfValue(), self.getPropValue()) == (True, 'Undefined'):          (True, False),  # Class-Specific Case 1

            # Proposition value definition:

            (self.getSelfValue(), self.getPropValue()) == (False, True):                (False, True),
            (self.getSelfValue(), self.getPropValue()) == (False, False):               (False, False),
            (self.getSelfValue(), self.getPropValue()) == (False, 'Undefined'):         (False, True),  # Class-Specific Case 2

            (self.getSelfValue(), self.getPropValue()) == ('Undefined', True):          (False, True),  # Special Case 1
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', False):         (True, False),  # Special Case 2

            # Standard 'else'
            
            (self.getSelfValue(), self.getPropValue()) == ('Undefined', 'Undefined'):   ('Undefined', 'Undefined')
        }
        self.setValues(self.Structure[True])
        self.check()
        
# Binary connectives:

class And(BinaryConnective):
    """And binary connective.

    Combines two elements and returns True if both of them are True.
    """
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
    """Or binary connective.

    Combines two elements and returns True if at least one of them is True.
    """
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
    """XOr binary connective.

    Combines two elements and returns True if only one of them is True.
    """
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
        self.check()

class Implicative(BinaryConnective):
    """Implicative binary connective.

    Combines two elements and returns True unless the first one is True and the
    second one is False.
    """
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
        self.check()

class BiImplicative(BinaryConnective):
    """Bi-implicative binary connective.

    Combines two elements and returns True only if both elements have the same
    value (either True or False).
    """
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
        self.check()
