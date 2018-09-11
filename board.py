from typing import List, Any, Iterable, Callable, Tuple, Generator
from copy import deepcopy
from operator import eq, ne, sub, add
from functools import partial
from itertools import zip_longest, takewhile, dropwhile, filterfalse


class WinnerException(Exception):
    def __init__(self, jorge: int) -> None:
        self.which_jorge = jorge


class BoardState:
    EMPTY_CELL = 0
    SIDE = 15
    MAX_SCORE = 2 ** 32

    def __init__(self, board: List[List[int]] = None):
        if board is None:
            board = [[BoardState.EMPTY_CELL for _ in range(
                BoardState.SIDE)] for _ in range(BoardState.SIDE)]
        self.board = board

    # def __getitem__(self, item):
    #     if isinstance(item, tuple):
    #         r, c = item
    #         return self.board[r][c]
    #     elif isinstance(item, int):
    #         return

    def is_valid(self, row: int, col: int)->bool:
        return (0 <= row < BoardState.SIDE) and (0 <= col < BoardState.SIDE) and (self.board[row][col] == 0)

    def possible_plays(self, player: int) -> Generator[Tuple[Tuple[int, int], 'BoardState'], None, None]:
        for i in range(BoardState.SIDE):
            for j in range(BoardState.SIDE):
                if self.board[i][j] == BoardState.EMPTY_CELL:
                    yield (i, j), self.after_play(i, j, player)

    def after_play(self, row: int, col: int, player: int) -> 'BoardState':
        assert self.board[row][col] == BoardState.EMPTY_CELL
        new_state = BoardState(board=deepcopy(self.board))
        new_state.board[row][col] = player
        return new_state

    def bound_count(self, start: Tuple[int, int], end: Tuple[int, int]):
        count = 0
        if all(map(lambda x: 0 <= x < 15, start)):
            count += 1 if self.board[start[0]][start[1]] else 0
        if all(map(lambda x: 0 <= x < 15, end)):
            count += 1 if self.board[end[0]][end[1]] else 0
        return count

    def det_row(self, jorge: int, start: Tuple[int, int], direction: Tuple[int, int])->List[Tuple[int, int]]:
        col_d, row_d = direction
        result = []

        def check(col: int, row: int):
            jorge_count = 0
            while (0 <= col < 15) and (0 <= row < 15):
                if self.board[row][col] != jorge:
                    break
                jorge_count += 1
                row += row_d
                col += col_d
            return jorge_count, (col, row)

        col, row = start
        while (0 <= col < 15) and (0 <= row < 15):
            jorge_count, end = check(col, row)
            if jorge_count:
                if jorge_count >= 5:
                    raise WinnerException(jorge)
                bounds = self.bound_count((col - col_d, row - row_d), end)
                if bounds < 2:
                    result.append((jorge_count, bounds))
            row += row_d
            col += col_d
        return result

    def detect_rows(self, jorge: int):
        def calculate_score(x)->int:
            n, b = x
            return 2 ** (3 * n - b)
        sequences = []
        for i in range(15):
            sequences.extend(self.det_row(jorge, (i, 0), (1, 0)))
            sequences.extend(self.det_row(jorge, (i, 0), (1, 1)))
            sequences.extend(self.det_row(jorge, (14 - i, 0), (-1, 1)))
            sequences.extend(self.det_row(jorge, (0, i), (0, 1)))
            sequences.extend(self.det_row(jorge, (0, 14 - i), (-1, 1)))
            sequences.extend(self.det_row(jorge, (0, i), (1, 1)))
        score = 0
        score += sum(map(calculate_score, sequences))
        return score

    def score(self, jorge: int, jorge_count: int):
        jorges_score = 0
        other_jorges_score = 0
        try:
            for some_jorge in range(1, jorge_count + 1):
                some_score = self.detect_rows(some_jorge)
                if some_jorge == jorge:
                    jorges_score = some_score
                else:
                    other_jorges_score = max(other_jorges_score, some_score)
        except WinnerException as winner:
            return BoardState.MAX_SCORE if winner.which_jorge == jorge else -BoardState.MAX_SCORE

        return jorges_score - other_jorges_score

    def __repr__(self):
        return '\n'.join(map(lambda r: ' '.join(map(str, r)), self.board))


