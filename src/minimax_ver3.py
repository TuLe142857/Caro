from typing import Callable, override
from state import *
from player import AI
import  pygame

import random

class MiniMaxVer3(AI):
    def __init__(
            self,
            evaluate_function:Callable[[State, str], int],
            depth:int,
            search_radius:int,
            extra_move:int
    ):

        self.eval_func = evaluate_function
        self.depth = max(1, depth)
        self.search_radius = max(1, search_radius)
        self.extra_move = max(1, extra_move)
        super().__init__(name=f"MiniMaxVer3(depth = {self.depth})")

    def find_valid_move(self, game_state:State)->list[tuple[int, int]]:
        all_moves = set()
        in_range = set()
        radius = [_ for _ in range(-self.search_radius, self.search_radius+1)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if game_state.cells[row][col] == EMPTY_CELL:
                    all_moves.add((row, col))
                    continue

                for dr in radius:
                    for dc in radius:
                        p = (row + dr, col + dc)
                        if (0 <= p[0] < BOARD_SIZE and 0 <= p[1] < BOARD_SIZE) \
                            and game_state.cells[p[0]][p[1]] == EMPTY_CELL:
                            in_range.add(p)

        out_range = all_moves-in_range
        moves_1 = list(in_range)
        moves_2 = random.sample(list(out_range), min(self.extra_move, len(out_range)))

        # print(f"move in range({len(moves_1)}):\n {moves_1}\nmove extra({len(moves_2)}):\n {moves_2}")
        # test = game_state.clone()
        # for m in moves_1:
        #     test.cells[m[0]][m[1]] = "_"
        # print(test)
        return moves_1 + moves_2
    def minimax(
            self,
            game_state:State,
            next_turn:str,
            depth_limit:int,
            alpha:int|float=float('-inf'),
            beta:int|float=float('inf')
    )->tuple[int|float, int]:
        """
        return tuple(best_eval, remain_depth_limit)

        """
        pygame.event.pump()
        if depth_limit == 0 or game_state.status() != NOT_FINISH:
            return self.eval_func(game_state, next_turn), depth_limit

        if next_turn == X_PIECE:
            best = (float('-inf'), 0)
            for move in self.find_valid_move(game_state):

                # execute ,move
                game_state.execute_move(move, next_turn)
                next_result = self.minimax(game_state=game_state, next_turn=O_PIECE, depth_limit=depth_limit-1, alpha=alpha, beta=beta)
                # undo move
                game_state.cells[move[0]][move[1]] = EMPTY_CELL

                # chon phuong an co eval max, neu eval bang nhau, chon phuong an gan nhat
                if (best[0] < next_result[0]) or (best[0] == next_result[0] and best[1] < next_result[1]):
                    best = next_result

                alpha = max(best[0], alpha)
                if beta <= alpha:
                    break
            return best

        else :
            best = (float('inf'), 0)
            for move in self.find_valid_move(game_state):

                # execute ,move
                game_state.execute_move(move, next_turn)
                next_result = self.minimax(game_state=game_state, next_turn=X_PIECE, depth_limit=depth_limit - 1,
                                           alpha=alpha, beta=beta)
                # undo move
                game_state.cells[move[0]][move[1]] = EMPTY_CELL

                # chon phuong an co eval min, neu eval bang nhau, chon phuong an gan nhat
                if (best[0] > next_result[0]) or (best[0] == next_result[0] and best[1] < next_result[1]):
                    best = next_result

                beta = min(best[0], beta)
                if beta <= alpha:
                    break
            return best


    @override
    def find_move(self, game_state:State, piece:str) ->tuple[int, int]:
        opponent = O_PIECE if piece==X_PIECE else X_PIECE
        moves = self.find_valid_move(game_state) if len(game_state.get_empty_cells()) != BOARD_SIZE**2 else game_state.get_empty_cells()
        random.shuffle(moves)
        print(f"move {BOARD_SIZE**2 - len(game_state.get_empty_cells()) + 1} total move in search:", len(moves) )
        # print(moves)
        best_eval = float('-inf') if piece == X_PIECE else float("inf")
        best_depth = 0
        best_move = moves[0]

        for move in moves:
            # execute move
            game_state.execute_move(move, piece)
            this_eval, this_depth = self.minimax(game_state=game_state, next_turn=opponent, depth_limit=self.depth-1)

            # undo move
            game_state.cells[move[0]][move[1]] = EMPTY_CELL

            # x turn => find max_eva
            if piece == X_PIECE:
                if (best_eval < this_eval) or (best_eval == this_eval and best_depth < this_depth):
                    best_eval = this_eval
                    best_depth = this_depth
                    best_move = move

            # o turn => find min eval
            else:
                if (best_eval > this_eval) or (best_eval == this_eval and best_depth < this_depth):
                    best_eval = this_eval
                    best_depth = this_depth
                    best_move = move
        # print(f"{self.name} best for {piece} in next {self.depth - best_depth} move is {best_move}, eval = {best_eval}")
        return best_move
# test
# if __name__ == '__main__':
#     state = State()
#     state.cells = [
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', 'O', 'X', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', 'X', 'O', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#         ['O', '.', '.', '.', '.', 'O', '.', '.', '.', '.']
#     ]
#
#     print(state)
#     sr = int(input("search radius: "))
#     ext = int(input("extra move: "))
#
#     m = MiniMaxVer3(
#         evaluate_function= (lambda gs, nt:10),
#         depth=1,
#         search_radius=sr,
#         extra_move=ext
#     )
#     moves = m.find_valid_move(game_state=state)
#     print(f"optimal move({len(moves)} moves):\n", moves)