from game import  Game
from player import Human
from state import  X_PIECE, O_PIECE
from evaluate import  eval_basic
from minimax import MiniMax

if __name__ == '__main__':
    human = Human(name="Tu")
    ai = MiniMax(name="Minimax", evaluate_function=eval_basic, depth=3)
    # PvP
    # game = Game(player_x=human, player_o=human, first_turn=X_PIECE)

    # PvAi
    game = Game(player_x=human, player_o=ai, first_turn=X_PIECE)

    # AivAi
    # game = Game(player_x=ai, player_o=ai, first_turn=X_PIECE)
    game.play()