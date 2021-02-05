""" EXERCISE 2
Suppose you have a list of all possible eye colors:

    eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")

Some other collection (say recovered from a database, or an external API) contains
a list of Person objects that have an eye color property.

Your goal is to create a dictionary that contains the number of people that have
the eye color as specified in eye_colors. The wrinkle here is that even if no
one matches some eye color, say amber, your dictionary should still contain an
entry "amber": 0.

Here is some sample data:

    class Person:
        def __init__(self, eye_color):
            self.eye_color = eye_color

    from random import seed, choices
    seed(0)
    persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]


As you can see we built up a list of Person objects, none of which should have
amber or blue eye colors

Write a function that returns a dictionary with the correct counts for each eye
color listed in eye_colors.
"""

from random import seed, choices
from collections import Counter
seed(0)


class Person:
    def __init__(self, eye_color):
        self.eye_color = eye_color

    def __repr__(self):
        return f'Person(eye_color={self.eye_color})'


eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")

# Generate data
persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]

def tally_eye_colors(persons, eye_colors):
    count = Counter({color : 0 for color in eye_colors}) #initializeo to zero
    count.update(person.eye_color for person in persons)
    return count.most_common()

print(tally_eye_colors(persons,eye_colors))