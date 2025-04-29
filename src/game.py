import pygame

from state import *
from player import *
from pygame_util import *

pygame.init()

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# mouse button
MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_SCROLL_UP = 4
MOUSE_SCROLL_DOWN = 5

# window size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 800

class Game:
    def __init__(self, player_x:Player, player_o:Player, first_turn:str=X_PIECE):
        # player & game state
        self.player_x = player_x
        self.player_o = player_o
        self.next_turn = first_turn
        self.state = State()

        # pygame screen, clock, fps
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60

        pygame.display.set_caption(f"{self.player_x}(X) vs {self.player_o}(O)")

        # game loop
        self.running = False

        # them bien nay de han che render lien tuc
        self.need_to_render = False

        # Component
        self.board = Board(10, 10)
        self.message_box = TextBox(
            x=10,
            y=self.board.height + self.board.y + 10,
            width=WINDOW_WIDTH - 20,
            height=WINDOW_HEIGHT - self.board.y - self.board.height - 20)

        self.components = [self.board, self.message_box]

    def wait_for_key_press(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
            self.clock.tick(self.fps)

    def next_player(self):
        if self.next_turn == X_PIECE:
            return self.player_x
        return self.player_o

    def make_move(self, move:tuple[int, int]):
        # print("make move call", self.next_turn, move)
        try:
            self.state.execute_move(position=move, piece=self.next_turn)
        except Exception as e:
            print(f"Can not put piece {self.next_turn} to position {move}")
            print(f"Exception message: {str(e)}")
            return

        if self.next_turn == X_PIECE:
            self.next_turn = O_PIECE
        else:
            self.next_turn = X_PIECE
        self.need_to_render = True

        # check game status after move
        status = self.state.status()
        message = ""
        if status != NOT_FINISH:
            if status == DRAW:
                message = "Draw! "
            elif status == X_WIN:
                message = f"{self.player_x}(X) win! "
            elif status == O_WIN:
                message = f"{self.player_o}(O) win! "
            message += "Press any key to exit"
            self.message_box.set_text(message)
            self.running = False
        else:
            message = f"It's {self.next_player()}({self.next_turn}) turn to move!"

        self.message_box.set_text(message)




    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.message_box.set_text("Press any key to exit")
                self.need_to_render = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                condition = self.board.contain_point(mx, my) \
                    and event.button == MOUSE_LEFT \
                    and isinstance(self.next_player(), Human)
                if condition:
                    self.make_move(self.board.mouse_click_at_cell(mx, my))


    def render(self):
        if not self.need_to_render:
            return

        # update game state
        self.board.set_state(self.state)

        # render
        self.screen.fill(WHITE)
        for c in self.components:
            c.render()
        pygame.display.update()

        self.need_to_render = False


    def play(self):
        self.running = True
        self.need_to_render = True

        self.message_box.set_text(f"It's {self.next_player()}({self.next_turn}) turn to move!")
        self.render()
        while self.running:
            # if next player is AI
            next_player = self.next_player()
            if isinstance(next_player, AI):
                move = next_player.find_move(self.state, self.next_turn)
                self.make_move(move)
            self.handle_event()
            self.render()
            self.clock.tick(self.fps)

        self.wait_for_key_press()
