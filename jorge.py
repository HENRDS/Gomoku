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
            return None, state.score(jorge, self.jorge_count)
        best_play: Tuple[int, int] = None
        new_depth = depth - 1
        is_my_turn = jorge == self.number
        next_jorge = 1 if jorge == self.jorge_count else jorge + 1
        for pos, st in state.possible_plays(next_jorge):
            _, val = self.minimax(st, alpha, beta, new_depth, next_jorge)
            if best_play is None:
                best_play = pos

            if is_my_turn:
                if val > alpha:
                    best_play = pos
                    alpha = val
            else:
                if val < beta:
                    best_play = pos
                    beta = val

            if alpha > beta:
                break

        # print(f'score: {(alpha if is_my_turn else beta)} {best_play}')
        # if best_play is None:
        #     raise Exception('Fuck man!')
        return best_play, (alpha if is_my_turn else beta)

    def play(self, state: BoardState) -> Tuple[int, int]:
        print('Jorge is thinking')
        pos, _ = self.minimax(state, -BoardState.MAX_SCORE, BoardState.MAX_SCORE, 3, self.number)
        print(f'Jorge will play {pos}')
        assert pos is not None
        return pos

    def __repr__(self):
        return f'Jorge {self.number}'
