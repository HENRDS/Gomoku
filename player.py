from board import BoardState
from typing import Tuple, Optional


class Player:
    def __init__(self, number: int, player_count = 2):
        self.number = number
        # Temos muitos Jorges aqui
        self.jorge_count = player_count

    def minimax(self,
                state: BoardState,
                alpha: int,
                beta: int,
                depth: int,
                jorge: int) -> Tuple[Optional[Tuple[int, int]], int]:
        if depth == 0:
            return None, state.score()
        best_play: Tuple[int, int]
        new_depth = depth + 1
        is_my_turn = jorge == self.number
        next_jorge = ((jorge + 1) % self.jorge_count) + 1
        for pos, st in state.possible_plays(next_jorge):
            _, val = self.minimax(st, alpha, beta, new_depth, next_jorge)
            if is_my_turn:
                if val > beta:
                    break
                if val > alpha:
                    best_play = pos
                    alpha = val
            else:
                if val < alpha:
                    break
                beta = min(val, beta)

        return best_play, alpha if is_my_turn else beta
