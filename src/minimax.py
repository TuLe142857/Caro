from typing import override, Callable
import  pygame
from state import *
from player import  AI
import  random


class MiniMax(AI):
    def __init__(self, name:str, evaluate_function:Callable[[State, str], float|int], depth:int=3):
        super().__init__(name + f"(depth={depth})")
        self.depth = depth
        self.evaluate_function = evaluate_function

    def minimax(
            self,
            game_state:State,
            next_turn:str,
            depth_limit:int,
            alpha:int|float=float('-inf'),
            beta:int|float=float('inf')
    )->int|float:

        pygame.event.pump()
        if depth_limit <= 0:
            depth_limit = 1
        if depth_limit == 0 or game_state.status() != NOT_FINISH:
            return self.evaluate_function(game_state, next_turn)

        # X move => find max
        if next_turn == X_PIECE:
            max_eval = float('-inf')
            for move in game_state.get_empty_cells():

                # make move & calculate
                game_state.execute_move(move, next_turn)
                current_eval = self.minimax(game_state=game_state, next_turn=O_PIECE, depth_limit=depth_limit-1, alpha=alpha, beta=beta)

                # undo move
                game_state.cells[move[0]][move[1]] = EMPTY_CELL

                max_eval = max(max_eval, current_eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        # O move => find min
        else:
            min_eval = float('inf')
            for move in game_state.get_empty_cells():

                game_state.execute_move(move, next_turn)
                current_eval = self.minimax(game_state=game_state, next_turn=X_PIECE, depth_limit=depth_limit-1, alpha=alpha, beta=beta)
                game_state.cells[move[0]][move[1]] = EMPTY_CELL

                min_eval = min(min_eval, current_eval)
                beta = min(min_eval, beta)
                if beta <= alpha:
                    break

            return  min_eval

    @override
    def find_move(self, game_state:State, piece:str) ->tuple[int, int]:
        opponent = O_PIECE if piece == X_PIECE else X_PIECE
        moves = game_state.get_empty_cells()
        random.shuffle(moves)
        best_choice = moves[0]
        best_eval = float('-inf') if piece == X_PIECE else float('inf')

        for move in moves:
            next_state = game_state.simulate_move(move, piece)
            current_eval = self.minimax(game_state=next_state, next_turn=opponent, depth_limit=self.depth-1)
            if (piece == X_PIECE and current_eval > best_eval) or (piece == O_PIECE and current_eval < best_eval):
                best_eval = current_eval
                best_choice = move
            if (piece == X_PIECE and best_eval == float('inf')) or (piece == O_PIECE and best_eval == float('-inf')):
                return best_choice
        print("best for", piece, "is", best_choice, "eval is", best_eval)
        return best_choice