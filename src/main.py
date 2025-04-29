from game import  Game
from player import Human
from state import  X_PIECE, O_PIECE
from minimax import MiniMax


from evaluate_basic import  evaluate_basic
from evaluate_ver2 import evaluate_ver2


if __name__ == '__main__':
    human = Human(name="Tu")
    # ai = MiniMax(name="Minimax", evaluate_function=evaluate_basic, depth=3)
    ai = MiniMax(name="Minimax", evaluate_function=evaluate_ver2, depth=2)
    # PvP
    # game = Game(player_x=human, player_o=human, first_turn=X_PIECE)

    # PvAi
    game = Game(player_x=human, player_o=ai, first_turn=X_PIECE)

    # AivAi
    # game = Game(player_x=ai, player_o=ai, first_turn=O_PIECE)
    game.play()