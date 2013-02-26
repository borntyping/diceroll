from functools import wraps

def series(func):
    """Wraps the functions return value in a DiceSeries"""
    @wraps(func)
    def return_diceseries(*args, **kwargs):
        return DiceSeries(func(*args, **kwargs))
    return return_diceseries

class DiceSeries(object):
    """An object that generates a series of dice combinations"""
    
    def __init__(self, generator):
        self.generator = generator

    def __iter__(self):
        return self

    def next(self):
        return self.generator.next()

    @series
    def __mul__(self, other):
        other = list(other)
        for a in self.generator:
            for b in other:
                yield a + b

    def __repr__(self):
        return "<{}: {}>".format(
            self.__class__.__name__, self.generator.__name__)

class Dice(object):
    @staticmethod
    def permutations(number, sides):
        """A recursive generator for all possible combinations of a dice set"""

        # For each side on the dice
        for s in xrange(1, sides+1):
            # If we are on the final die
            if number == 1:
                yield (s,)
            else:
                # Yield the current side and the recursive combinations
                for d in Dice.permutations(number-1, sides):
                    yield (s,) + d
    
    def __init__(self, number, sides):
        self.number = number
        self.sides = sides

    def __len__(self):
        """The number of possible combinations (s^n)"""
        return self.sides ** self.number

    @series
    def __iter__(self):
        """Return a series of all possible permutations"""
        return Dice.permutations(self.number, self.sides)

    def __repr__(self):
        return "<{}: {}d{}>".format(
            self.__class__.__name__, self.number, self.sides)

permutation_list = [(1, 1), (1, 2), (2, 1), (2, 2)]
assert permutation_list == list(Dice(2, 2))
assert permutation_list == list(Dice.permutations(2, 2))
assert permutation_list == list(DiceSeries(Dice.permutations(2, 2)))
assert permutation_list == list(DiceSeries(iter(Dice(2,2))))

# Assert __len__ is calculated correctly
assert len(Dice(2,2)) == len(list(Dice(2, 2))) == len(permutation_list)

# Assert 1d2 * 1d2 is equivalent to 2d2
assert permutation_list == list(iter(Dice(1, 2)) * iter(Dice(1, 2)))
