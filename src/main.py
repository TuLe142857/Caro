from game import  Game
from player import Human
from state import  X_PIECE, O_PIECE
from minimax import MiniMax
from minimax_optimal import MiniMaxOptimal

from evaluate_basic import  evaluate_basic
from evaluate_ver2 import evaluate_ver2


if __name__ == '__main__':
    human = Human(name="Tu")
    ai = MiniMax(name="Minimax", evaluate_function=evaluate_ver2, depth=2)
    ai_ver2 = MiniMaxOptimal(evaluate_function=evaluate_ver2, depth=2, search_radius=1, max_extra_move=2)
    # PvP
    # game = Game(player_x=human, player_o=human, first_turn=X_PIECE)

    # PvAi
    game = Game(player_x=ai_ver2, player_o=human, first_turn=X_PIECE)

    # AivAi
    # game = Game(player_x=ai_ver2, player_o=ai, first_turn=O_PIECE)
    game.play()