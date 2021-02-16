""" PROJECT 2
Special Mod class.
- assume n is a positive integer, assume a and b are integers
- the residue of a number a mod n is a % n.
- two numbers a and b are said to be congruent modulo n: a = b (mod n)
  if their residues are equal, i.e. a % n = b % n
Create a class called Mod.
- initialize with value and modulus arguments.
    - ensure modulus and value are both integers
    - ensure modulus is positive
    - store the value as the residue
- implement congruence for the == operator
    - allow comparison of Mod object to an int (in which case use residue of int)
    - allow comparison of two Mod objects only if they have the same modulus
    - ensure objects remain hashable
- provide an implementation so that int(mod_object) will return the residue
- provide a proper representation (repr)
- implement the operators: +, -, *, **
    - support other operand to be Mod (with same modulus only)
    - support other operand to be an integer (and use the same modulus)
    - always return a Mod instance
        - perform the +, -, *, ** operations on the values (so there's nothing complicated here)
            i.e. Mod(2, 3) + 16 -> Mod (2+16, 3) -> Mod(0, 3)
- implement the corresponding in-place arithmetic operators
- implement ordering (makes sense since we compare residues)
    - support other operand to be a Mod (with same modulus) or an integer
"""
from functools import total_ordering
import operator

@total_ordering
class Mod:
    def __init__(self, value, modulus):
        if not isinstance(value, int):
            raise ValueError('value must be an integer.')
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError('modulus must be positive integer.')
        self._modulus = modulus
        self._value = value % modulus

    @property
    def modulus(self):
        return self._modulus

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f'Mod({self.value}, {self.modulus})'

    def __int__(self):
        return int(self._value)

    def _get_value(self, other):
        if isinstance(other, Mod) and self.modulus == other.modulus:
            return other.value
        if isinstance(other, int):
            return other % self.modulus
        return TypeError('Incompatible types.')
    
    def _perform_operation(self, other, op, *, inplace=False):
        other_value = self._get_value(other)
        new_value = op(self.value, other_value)
        if inplace:
            self.value = new_value % self.modulus
            return self
        else:
            return Mod(new_value, self.modulus)

    def __eq__(self, other):
        if isinstance(other, Mod) and self.modulus == other.modulus:
            return self.value == other.value
        if isinstance(other, int):
            return other % self.modulus == self.value
        return NotImplemented

    def __hash__(self):
        return hash((self.value, self.modulus))

    def __neg__(self):
        return Mod(-self.value, self.modulus)

    def __add__(self, other):
        return self._perform_operation(other, operator.add)
    
    def __iadd__(self, other):
        return self._perform_operation(other, operator.add, inplace=True)
    
    def __sub__(self, other):
        return self._perform_operation(other, operator.sub)
    
    def __isub__(self, other):
        return self._perform_operation(other, operator.sub, inplace=True)
    
    def __mul__(self, other):
        return self._perform_operation(other, operator.mul)

    def __imul__(self, other):
        return self._perform_operation(other, operator.mul, inplace=True)

    def __pow__(self, other):
        return self._perform_operation(other, operator.pow)

    def __ipow__(self, other):
        return self._perform_operation(other, operator.pow, inplace=True)
        
    def __lt__(self, other):
        other_value = self._get_value(other)
        return self.value < other_value

