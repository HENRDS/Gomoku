from board import BoardState
from typing import Tuple, Optional
# Temos muitos Jorges aqui


class Jorge:
    def __init__(self, number: int, jorge_count=2):
        self.number = number
        self.jorge_count = jorge_count

    def minimax(self,
                state: BoardState,
                alpha: int,
                beta: int,
                depth: int,
                jorge: int) -> Tuple[Optional[Tuple[int, int]], int]:
        if depth == 0:
            return None, state.score()
        best_play: Tuple[int, int]
        new_depth = depth - 1
        is_my_turn = jorge == self.number
        next_jorge = ((jorge + 1) % self.jorge_count) + 1
        for pos, st in state.possible_plays(next_jorge):
            _, val = self.minimax(st, alpha, beta, new_depth, next_jorge)
            if is_my_turn:
                if val > alpha > beta:
                    break
                if val > alpha:
                    best_play = pos
                    alpha = val
            else:
                if val < alpha:
                    break

                beta = min(val, beta)
        return best_play, alpha if is_my_turn else beta

    def play(self, state: BoardState) -> Tuple[int, int]:
        max_score = int(2 ** 31)
        pos, _ = self.minimax(state, max_score, -max_score, 3, self.number)
        assert pos is not None
        return pos

    def __repr__(self):
        return f'Jorge {self.number}'
