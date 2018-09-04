from typing import List
from operator import eq
from collections import Counter


class BoardState:
    EMPTY_CELL = 0
    SIDE = 15

    def __init__(self, board: List[List[int]] = None):
        if board is None:
            board = [[BoardState.EMPTY_CELL for _ in range(
                BoardState.SIDE)] for _ in range(BoardState.SIDE)]
        self.board = board

    def check_lines(self, jorge: int):
        def count(lst: List[int], *vals: int) -> int:
            assert len(lst) > len(vals)
            n = 0
            pattern_len = len(vals)
            for cur in range(len(lst) - pattern_len):
                if all(map(eq, zip(vals, lst[cur: cur + pattern_len]))):
                    n += 1
            return n

        open_3 = capped_3 = open_4 = gaped_22 = consec_5 = gaped_3 = 0
        other_jorge = 1 if jorge == 2 else 2
        no_jorge = 0
        for i in range(BoardState.SIDE):
            row = self.board[i]
            open_3 += count(row, jorge, jorge, jorge)
            capped_3 += count(row, jorge, jorge, jorge, other_jorge)
            gaped_22 += count(row, jorge, jorge, no_jorge, jorge, jorge)
            open_4 += count(row, other_jorge, other_jorge, other_jorge, other_jorge, jorge)
            col = [r[i] for r in self.board]
            consec_5 += count(col, jorge, jorge, jorge, jorge, jorge)
            gaped_3 += count(col, jorge, jorge, no_jorge, jorge)


    def check_cols(self, jorge: int):
        capped_4 = gaped_4 = 0

    def score(self)-> int:
        pass
