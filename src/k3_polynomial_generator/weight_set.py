class WeightSet:
    def __init__(self, weights: list[str]):
        assert len(weights) == 5
        self.weights = [int(w) for w in weights]

    def __str__(self):
        return f"({self.weights[0]}, {self.weights[1]}, {self.weights[2]}, {self.weights[3]}; {self.weights[4]})"

    def __repr__(self):
        return str(self)

    def get(self, index) -> int:
        return self.weights[index]

    def get_total(self) -> int:
        return self.get(4)

    def get_all_weights(self) -> list[int]:
        return self.weights[:len(self.weights) - 1]
