class Term:
    symbols = ["x", "y", "z", "w"]

    def __init__(self, index: int, exponents: list[int]):
        self.index = index
        self.exponents = exponents

    def __str__(self):
        term_str = Term.symbols[self.index]
        if self.exponents[self.index] != 1:
            term_str += f"^{self.exponents[self.index]}"

        for i in range(len(self.exponents)):
            if i == self.index:
                continue
            if self.exponents[i]:
                term_str += Term.symbols[i]

        return term_str

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.index == other.index and self.exponents == other.exponents

    def is_compatible_with(self, other) -> bool:
        if other.index == self.index:
            return False

        for i in range(len(self.exponents)):
            if i == self.index or i == other.index:
                continue
            if self.exponents[i] == 1 and other.exponents[i] == 1:
                return False

        return True

    def get_exponents(self) -> list[int]:
        return self.exponents

    def get_index(self) -> int:
        return self.index


class Polynomial:
    def __init__(self, terms: list[Term]):
        self.terms = terms

    def __str__(self):
        return " + ".join([str(term) for term in self.terms])

    def __repr__(self):
        return self.__str__()
    
    def get_exponent_matrix(self):
        return [term.get_exponents() for term in self.terms]
