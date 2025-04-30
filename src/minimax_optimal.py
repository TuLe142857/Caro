from typing import override, Callable
import  pygame
from state import *
from player import  AI
import  random


def find_valid_move(game_state:State, sr:int, extra_move:int)->list[tuple[int, int]]:
    """
    sr: search radius
    return moves: [all in_range] + [1 phan out_range]
    pham vi tim kiem: ban kinh <<sr>> o ke tu cac o co gia tri(value != empty cell)
    in_range: danh sach cac o trong trong pham vi tim keim
    out_range: danh sach cac o trong ngoai pham vi tim kiem
    """

    in_range = set()
    out_range = set(game_state.get_empty_cells())

    directions = [(sr, 0), (-sr, 0), (0, sr), (0, -sr), (sr, sr), (-sr, -sr), (sr, -sr), (-sr, sr)]
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_state.cells[row][col] == EMPTY_CELL:
                continue
            # print(f"around ({row}, {col}):")
            for d in directions:
                p = (row+d[0], col+d[1])
                if (0 <= p[0] < BOARD_SIZE and 0 <= p[1] < BOARD_SIZE)\
                    and game_state.cells[p[0]][p[1]] == EMPTY_CELL:
                    in_range.add(p)
                    # print(d, p)

    out_range = out_range-in_range

    moves_1 = list(in_range)
    moves_2= random.sample(list(out_range), min(extra_move, len(out_range)))

    # print("in range:\n", moves_1, '\nOut range:\n', moves_2 )
    return  moves_1 + moves_2



class MiniMaxOptimal(AI):
    def __init__(self, evaluate_function:Callable[[State, str], float|int], depth:int=3, search_radius:int=1, max_extra_move:int=3):
        """
        evaluate_function: ham danh gia trang thai ban co
        depth: gioi han do sau tim kiem
        search_radius: ban kinh tim kiem(tim kiem cac nuoc di hop le xung quanh cac o da dat quan)
        max_extra_move: se lay ngau nhien 1 vai nuoc di ben ngoai pham vi tim kiem

        """
        super().__init__(f"MiniMaxOptimal (depth={depth})")
        self.depth = depth
        self.evaluate_function = evaluate_function
        self.search_radius = search_radius
        if max_extra_move ==0 :
            max_extra_move = 1
        self.max_extra_move = max_extra_move

    def minimax(
            self,
            game_state:State,
            next_turn:str,
            depth_limit:int,
            alpha:int|float=float('-inf'),
            beta:int|float=float('inf')
    )->int|float:

        pygame.event.pump()
        if depth_limit == 0:
            return self.evaluate_function(game_state, next_turn)

        # X move => find max
        if next_turn == X_PIECE:
            max_eval = float('-inf')
            for move in find_valid_move(game_state=game_state, sr=self.search_radius, extra_move=self.max_extra_move):
                # make move & calculate
                game_state.execute_move(move, next_turn)
                status = game_state.check_win_at_cell(move[0], move[1])
                if status != NOT_FINISH:
                    current_eval = float('inf') if status == X_WIN else float('-inf') if status == O_WIN else 0
                else:
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
            for move in find_valid_move(game_state=game_state, sr=self.search_radius, extra_move=self.max_extra_move):
                # make move & calculate
                game_state.execute_move(move, next_turn)
                status = game_state.check_win_at_cell(move[0], move[1])
                if status != NOT_FINISH:
                    current_eval = float('inf') if status == X_WIN else float('-inf') if status == O_WIN else 0
                current_eval = self.minimax(game_state=game_state, next_turn=X_PIECE, depth_limit=depth_limit-1, alpha=alpha, beta=beta)

                # undo move
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
        # moves  = find_valid_move(game_state=game_state, sr=self.search_radius, extra_move=self.max_extra_move)
        random.shuffle(moves)
        best_choice = moves[0]
        best_eval = float('-inf') if piece == X_PIECE else float('inf')

        for move in moves:
            next_state = game_state.simulate_move(move, piece)
            current_eval = self.minimax(game_state=next_state, next_turn=opponent, depth_limit=self.depth)
            if (piece == X_PIECE and current_eval > best_eval) or (piece == O_PIECE and current_eval < best_eval):
                best_eval = current_eval
                best_choice = move
            if (piece == X_PIECE and best_eval == float('inf')) or (piece == O_PIECE and best_eval == float('-inf')):
                return best_choice
        print("best for", piece, "is", best_choice, "eval is", best_eval)
        return best_choice


# test
if __name__ == '__main__':
    state = State()
    state.cells = [
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'O', 'X', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'X', 'O', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['O', '.', '.', '.', '.', 'O', '.', '.', '.', '.']
    ]

    print(state)
    sr = int(input("search radius: "))
    ext = int(input("extra move: "))

    moves = find_valid_move(game_state=state, sr=sr, extra_move=ext)
    print(f"optimal move({len(moves)} moves):\n", moves)