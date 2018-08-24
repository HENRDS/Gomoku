from typing import List
from operator import eq
from itertools import zip_longest


class BoardState:
    EMPTY_CELL = -1
    SIDE = 15

    def __init__(self, board: List[List[int]] = None):
        if board is None:
            board = [[BoardState.EMPTY_CELL] * BoardState.SIDE] * BoardState.SIDE
        self.board = board

    def __getitem__(self, item) -> int:
        try:
            i, j = item
            return self.board[i][j]
        except ...:
            raise KeyError(item)

    def count(self, lst: List[int], *vals: int):
        res = 0
        nn = 0
        for i, n in enumerate(lst):
            if i < nn:
                continue
            if all(map(eq, zip_longest(vals, lst[i: i+len(vals)]))):
                nn = i + len(vals)
                res += 1
        return res


    def check_lines(self, jorge: int):
        open_3 = capped_3 = open_4 = gapped_22 = consec_5 = gapped_3 = 0
        other_jorge = 1 if jorge == 2 else 2
        no_jorge = 0
        for i in range(len(self.board)):
            row = self.board[i]
            open_3 += self.count(row, jorge, jorge, jorge)
            capped_3 += self.count(row, jorge, jorge, jorge, other_jorge)
            gapped_22 += self.count(row, jorge, jorge, no_jorge, jorge, jorge)
            open_4 += self.count(row, other_jorge, other_jorge, other_jorge, other_jorge, jorge)
            col = [r[i] for r in self.board]
            consec_5 += self.count(col, jorge, jorge, jorge, jorge, jorge)
            gapped_3 += self.count(col, jorge, jorge, no_jorge, jorge)



    def check_cols(self, jorge: int):
        capped_4 = gapped_4 = 0




    def score(self):
        pass

b = BoardState()
print(b[2, 3])


