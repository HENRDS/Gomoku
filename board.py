from typing import List, Any, Iterable, Callable, Tuple, Generator, Dict
from copy import deepcopy
from operator import add


class WinnerException(Exception):
    def __init__(self, jorge: int) -> None:
        self.which_jorge = jorge


class BoardState:
    EMPTY_CELL = 0
    SIDE = 15
    MAX_SCORE = 2 ** 32
    LOOK_AREA = [
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    ]

    def __init__(self, board: Dict[Tuple[int, int], int] = None):
        if board is None:
            board: Dict[Tuple[int, int], int] = {}
        self.board = board

    def __getitem__(self, item):
        if isinstance(item, tuple):
            r, c = item
            if (0 <= r < BoardState.SIDE) and (0 <= c < BoardState.SIDE):
                return self.board.get((r, c), BoardState.EMPTY_CELL)
            raise IndexError(r, c)
        raise ValueError(item)

    def is_valid(self, row: int, col: int)->bool:
        return (0 <= row < BoardState.SIDE) and (0 <= col < BoardState.SIDE) \
               and self.board.get((row, col), BoardState.EMPTY_CELL) == BoardState.EMPTY_CELL

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            r, c = key
            if self.is_valid(r, c):
                self.board[r, c] = value
            else:
                raise IndexError(r, c)
        else:
            raise ValueError()

    def possible_plays(self, player: int) -> Generator[Tuple[Tuple[int, int], 'BoardState'], None, None]:
        visited = set()
        queue: List[Tuple[int, int]] = list(self.board.keys())
        while queue:
            cur = queue.pop()
            for delta in BoardState.LOOK_AREA:
                pos = tuple(map(add, cur, delta))
                if pos in visited:
                    continue
                if self.is_valid(*pos):
                    queue.append(pos)
                    yield pos, self.after_play(*pos, player)
                visited.add(pos)

    def after_play(self, row: int, col: int, player: int) -> 'BoardState':
        new_state = BoardState(board=deepcopy(self.board))
        new_state[row, col] = player
        return new_state

    def bound_count(self, start: Tuple[int, int], end: Tuple[int, int]):
        count = 0
        if all(map(lambda x: 0 <= x < 15, start)):
            count += 1 if self[start] else 0
        if all(map(lambda x: 0 <= x < 15, end)):
            count += 1 if self[end] else 0
        return count

    def det_row(self, jorge: int, start: Tuple[int, int], direction: Tuple[int, int])->List[Tuple[int, int]]:
        row_d, col_d = direction
        result = []

        def check(_row: int, _col: int):
            jorge_count = 0
            while (0 <= _col < 15) and (0 <= _row < 15):
                if self[_row, _col] != jorge:
                    break
                jorge_count += 1
                _row += row_d
                _col += col_d
            return jorge_count, (_row, _col)
        row, col = start
        while (0 <= col < 15) and (0 <= row < 15):
            jorge_count, end = check(row, col)
            if jorge_count:
                if jorge_count >= 5:
                    raise WinnerException(jorge)
                bounds = self.bound_count((row - row_d, col - col_d), end)
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
            sequences.extend(self.det_row(jorge, (i, 0), (0, 1)))
            sequences.extend(self.det_row(jorge, (0, i), (1, 0)))

            sequences.extend(self.det_row(jorge, (i, 0), (1, 1)))
            sequences.extend(self.det_row(jorge, (0, i), (1, 1)))

            sequences.extend(self.det_row(jorge, (0, 14 - i), (1, -1)))
            sequences.extend(self.det_row(jorge, (i, 14), (1, -1)))
        score = 0
        score += sum(map(calculate_score, sequences))
        return score

    def score(self, jorge: int, jorge_count: int, sub_others= True):
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
        if sub_others:
            return jorges_score - other_jorges_score
        return jorges_score

    def __repr__(self):
        return repr(self.board)
