from state import *

def eval_basic(game_state:State, next_turn:str)->int|float:
    status = game_state.status()
    if status == X_WIN:
        return float('inf')
    elif status == O_WIN:
        return float('-inf')
    elif status == DRAW:
        return 0
    return 0

