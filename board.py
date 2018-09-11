from typing import List, Any, Iterable, Callable, Tuple, Generator
from copy import deepcopy
from operator import eq, ne
from functools import partial
from itertools import zip_longest, takewhile, dropwhile, filterfalse


class BoardState:
    EMPTY_CELL = 0
    SIDE = 15

    def __init__(self, board: List[List[int]] = None):
        if board is None:
            board = [[BoardState.EMPTY_CELL for _ in range(
                BoardState.SIDE)] for _ in range(BoardState.SIDE)]
        self.board = board

    def possible_plays(self, player: int) -> Generator[((int, int), 'BoardState'), None, None]:
        for i in range(BoardState.SIDE):
            for j in range(BoardState.SIDE):
                if self.board[i][j] == BoardState.EMPTY_CELL:
                    yield (i, j), self.after_play(i, j, player)

    def after_play(self, row: int, col: int, player: int) -> 'BoardState':
        assert self.board[row][col] == BoardState.EMPTY_CELL
        new_state = BoardState(board=deepcopy(self.board))
        new_state.board[row][col] = player
        return new_state

    def is_bounded(self, board, y_end, x_end, length, d_y, d_x):
        bound_end_y = y_end + d_y
        bound_end_x = x_end + d_x
        bound_beg_y = y_end - length * d_y
        bound_beg_x = x_end - length * d_x

        open_range = range(0, 15)

        if bound_end_y in open_range and bound_end_x in open_range and bound_beg_y \
                in open_range and bound_beg_x in open_range:

            bound_end = board[bound_end_y][bound_end_x]
            bound_beg = board[bound_beg_y][bound_beg_x]

            if bound_end == 0 and bound_beg == 0:
                bound = "OPEN"
            elif (bound_end == 0) ^ (bound_beg == 0):
                bound = "SEMIOPEN"
            else:
                bound = "CLOSED"

        else:
            if bound_end_y in open_range and bound_end_x in open_range:
                bound_end = board[bound_end_y][bound_end_x]

                if bound_end == 0:
                    bound = "SEMIOPEN"
                else:
                    bound = "CLOSED"


            elif bound_beg_y in open_range and bound_beg_x in open_range:
                bound_beg = board[bound_beg_y][bound_beg_x]

                if bound_beg == 0:
                    bound = "SEMIOPEN"
                else:
                    bound = "CLOSED"

            else:
                bound = "CLOSED"

        return bound

    def detect_row(self, board, col, y_start, x_start, length, d_y, d_x):
        open_seq_count, semi_open_seq_count = 0, 0

        y = y_start
        x = x_start

        len = 0

        while x in range(15) and y in range(15):
            if board[y][x] == col:

                while (y + len * d_y < 15) and (x + len * d_x < 15):
                    if board[y + len * d_y][x + len * d_x] == col:
                        len += 1
                    else:
                        break

                if len == length:
                    y_end = y + (length - 1) * d_y
                    x_end = x + (length - 1) * d_x
                    if self.is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    if self.is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1

            if len == 0:
                x += d_x
                y += d_y
            else:
                y += len * d_y
                x += len * d_x
            len = 0

        return open_seq_count, semi_open_seq_count

    def det_rows(self, board, col, length):
        open_seq, semi_open_seq = 0, 0

        for i in range(15):
            open_seq += self.detect_row(board, col, i, 0, length, 0, 1)[0]
            semi_open_seq += self.detect_row(board, col, i, 0, length, 0, 1)[1]

            open_seq += self.detect_row(board, col, 0, i, length, 1, 0)[0]
            semi_open_seq += self.detect_row(board, col, 0, i, length, 1, 0)[1]

            open_seq += self.detect_row(board, col, 14 - i, 0, length, 1, 1)[0]
            semi_open_seq += self.detect_row(board, col, 14 - i, 0, length, 1, 1)[1]

            open_seq += self.detect_row(board, col, i, 14, length, 1, -1)[0]
            semi_open_seq += self.detect_row(board, col, i, 14, length, 1, -1)[1]

            if i < 14:
                open_seq += self.detect_row(board, col, 0, i + 1, length, 1, 1)[0]
                semi_open_seq += self.detect_row(board, col, 0, i + 1, length, 1, 1)[1]

                open_seq += self.detect_row(board, col, 0, 13 - i, length, 1, -1)[0]
                semi_open_seq += self.detect_row(board, col, 0, 13 - 1, length, 1, -1)[1]

        return open_seq, semi_open_seq

    def score(self):
        board = self.board
        MAX_SCORE = 247338

        open_b = {}
        semi_open_b = {}
        open_w = {}
        semi_open_w = {}

        for i in range(2, 7):
            open_b[i], semi_open_b[i] = self.det_rows(board, 1, i)
            open_w[i], semi_open_w[i] = self.det_rows(board, 2, i)

        if open_b[5] >= 1 or semi_open_b[5] >= 1:
            return -MAX_SCORE

        elif open_w[5] >= 1 or semi_open_w[5] >= 1:
            return MAX_SCORE

        return (16384 * open_w[4] +
                8196 * semi_open_w[4] +
                -16384 * open_b[4] +
                -8196 * semi_open_b[4] +
                1024 * open_w[3] +
                512 * semi_open_w[3] +
                -1024 * open_b[3] +
                -512 * semi_open_b[3] +
                -64 * open_b[2] +
                -32 * semi_open_b[2] +
                64 * open_w[2] +
                32 * semi_open_w[2])



    # def detect_row(self, row_index: int, player: int):
    #     def split(lst: Iterable[Any], pred: Callable[[Any], bool]) -> Tuple[List[Any], List[Any]]:
    #         fst = list(takewhile(pred, lst))
    #         snd = lst[len(fst):]
    #         return fst, snd
    #     row = self.board[row_index]
    #     score = 0
    #     left_closed = False
    #     while row:
    #         if row[0] == player:
    #             sequence, row = split(row, partial(eq, player))
    #             seq_len = len(sequence)
    #             if row:
    #                 if row[0] != 0:
    #                     score += 2 * seq_len
    #                 elif left_closed:
    #                     score += seq_len
    #                 else:
    #                     score += seq_len * 2 ** seq_len
    #         elif row[0] == 0:
    #             row = list(dropwhile(partial(eq, 0), row))
    #             left_closed = False
    #         else:
    #             row = list(dropwhile(partial(ne, player), row))
    #             left_closed = True
    #     return score

    def __repr__(self):
        return '\n'.join(map(lambda r: ' '.join(map(str, r)), self.board))


if __name__ == '__main__':
    b = BoardState()
    b.board[0][1:7] = [1, 1, 2, 1, 1, 2]
    print(b.detect_row(0, 1))
    print (b)
