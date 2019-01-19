import numpy as np


class OutputChars:
    """
    Decode our output from one-hot vector to numbers
    """
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, s, num_rows):
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(s):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)


class InputChars:
    """
    Encode input string into vectors
    """
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, s):
        return [self.to_index(c) for c in s]

    # if unseen char, treat as space
    def to_index(self, c):
        if c in self.char_indices:
            return self.char_indices[c] + 1
        return self.char_indices[" "] + 1


class Colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'


if __name__ == '__main__':
    pass
