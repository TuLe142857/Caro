from player import AI
from state import *


def make_game(x:AI, o:AI, first_move:str):
    gs = State()
    piece = first_move
    while gs.status() == NOT_FINISH:
        player = x if piece == X_PIECE else o
        gs.execute_move(player.find_move(gs, piece), piece)
        piece = X_PIECE if piece == O_PIECE else O_PIECE
    return gs.status()
def statistic(player_o:AI, player_x:AI, n_game:int):
    first_turn = X_PIECE
    xw = 0
    ow = 0
    dr = 0
    print(f"{player_x} vs {player_o} in {n_game} games")
    for i in range(n_game):
        result = make_game(x=player_x, o=player_o, first_move=first_turn)
        first_turn = X_PIECE if first_turn==O_PIECE else O_PIECE
        if result == X_WIN:
            print(f"game {i+1}: {player_x} win")
            xw += 1
        elif result == O_WIN:
            print(f"game {i + 1}: {player_o} win")
            ow += 1
        else:
            print(f"game {i + 1}: draw")
            dr += 1
    return xw, ow, dr