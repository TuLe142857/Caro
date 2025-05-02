from game import  Game
from player import Human, AI
from state import  X_PIECE, O_PIECE
from minimax import MiniMax
from minimax_optimal import MiniMaxOptimal
from minimax_ver3 import  MiniMaxVer3

from evaluate_basic import  evaluate_basic
from evaluate_ver2 import evaluate_ver2
from state import *

if __name__ == '__main__':
    human = Human(name="Tu")
    ai = MiniMax(name="Minimax", evaluate_function=evaluate_ver2, depth=2)
    ai_ver2 = MiniMaxOptimal(evaluate_function=evaluate_ver2, depth=3, search_radius=1, max_extra_move=2)
    ai_ver2_d3 = MiniMaxOptimal(evaluate_function=evaluate_ver2, depth=4, search_radius=1, max_extra_move=2)

    ai_ver3 = MiniMaxVer3(evaluate_function=evaluate_ver2, depth=4, search_radius=1, extra_move=1)
    ai_ver3_d3 = MiniMaxVer3(evaluate_function=evaluate_ver2, depth=3, search_radius=1, extra_move=1)

    # PvP
    # game = Game(player_x=human, player_o=human, first_turn=X_PIECE)

    # PvAi
    game = Game(player_x=ai_ver3, player_o=human, first_turn=X_PIECE, evaluate_function=evaluate_ver2)

    # AivAi
    # game = Game(player_x=ai_ver3_d3, player_o=ai_ver3, first_turn=O_PIECE, evaluate_function=evaluate_ver2)

    game.play()
