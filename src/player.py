import  state

class Player:
    def __init__(self, name:str):
        self.name = name

    def __str__(self):
        return self.name


class Human(Player):
    def __int__(self, name:str):
        super().__init__(name)

class AI(Player):
    def __int__(self, name):
        super().__init__(name)

    def find_move(self, game_state:state.State, piece:str)->tuple[int, int]:
        pass