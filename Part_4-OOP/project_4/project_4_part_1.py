"""PROJECT 4: Descriptors
Part 1:
Write two data descriptors to validate the values to be used in a class:
    IntegerField: only allows integral numbers between a min and max value (default None)
    CharField: only allows string with a min and max length (default None)
e.g. we want to use the descriptors as:
    class Person:
        name = CharField(1, 50)
        age = IntegerField(0, 200)
Notice there is repitition though. Which brings us to Part 2...

Part 2:
To avoid repetition, make a base class called BaseValidator to inherit from.
"""

class IntegerField:
    def __init__(self, min_, max_):
        self._min = min_
        self._max = max_

    def __set_name__(self, owner_class, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f'{self.name} must be an integer.')
        if self._min is not None and value < self._min:
            raise ValueError(f'{self.name} cannot be less than {self._min}.')
        if self._max is not None and value > self._max:
            raise ValueError(f'{self.name} cannot be greater than {self._max}.')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner_class):
        if isinstance is None:
            return self
        return instance.__dict__.get(self.name)


class CharField:
    def __init__(self, min_=None, max_=None):
        min_ = min_ or 0
        min_ = max(min_, 0) #replace negative value with zero
        self._min = min_
        self._max = max_

    def __set_name__(self, owner_class, prop_name):
        self.prop_name = prop_name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'{self.prop_name} must be a string.')
        if self._min is not None and len(value) < self._min:
            raise ValueError(f'{self.prop_name} must contain at least {self._min} characters.')
        if self._max is not None and len(value) > self._max:
            raise ValueError(f'{self.prop_name} cannot contain more than {self._max} characters.')
        instance.__dict__[self.prop_name] = value

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.prop_name)
