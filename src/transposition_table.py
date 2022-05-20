class TTEntry:
    def __init__(self, alpha: int, beta: int, score: int, state: int) -> None:
        self.alpha = alpha
        self.beta = beta
        self.score = score
        self.state = state


class TranspositionTable(dict):
    def __init__(self, mod: int):
        self.mod = mod
        super().__init__()

    def modkey(self, key: int) -> int:
        return key % self.mod

    def __getitem__(self, key: int) -> TTEntry:
        return super().__getitem__(self.modkey(key))

    def __setitem__(self, key: int, entry: TTEntry) -> None:
        return super().__setitem__(self.modkey(key), entry)

    def __contains__(self, key: int) -> bool:
        return super().__contains__(self.modkey(key))
