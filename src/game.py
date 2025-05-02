from collections.abc import Callable
from json.encoder import py_encode_basestring_ascii

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
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

def normalize_eval(evaluate:int|float)->tuple[float, float]:
    ratio_x = 0.0
    ratio_o = 0.0
    near_max = 10.0**9
    if evaluate == float('inf'):
        ratio_x = 1.0
    elif evaluate == float('-inf'):
        ratio_o = 1.0
    else:
        ratio_x = max(0.1, min(1.0,(evaluate+near_max)/(2*near_max)))
    ratio_o = 1.0 - ratio_x
    return ratio_x, ratio_o

class Game:
    def __init__(
            self,
            player_x:Player,
            player_o:Player,
            first_turn:str=X_PIECE,
            evaluate_function:Callable[[State, str], int]|None=None
    ):
        """

        """
        '''
        -------------------------------------------------
        |               PLAYERS & GAME STATE            |
        -------------------------------------------------
        '''
        # player & game state
        self.player_x = player_x
        self.player_o = player_o
        self.first_turn = first_turn
        self.eval_func = evaluate_function

        self.next_turn = first_turn
        self.state = State()
        self.match_record = []

        '''
        -------------------------------------------------
        |        PYGAME SCREEN, CLOCK, FPS, ...         |
        -------------------------------------------------
        '''
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = False
        self.need_to_render = False
        pygame.display.set_caption(f"{self.player_x}(X) vs {self.player_o}(O)")

        '''
        -------------------------------------------------
        |               COMPONENTS                      |
        -------------------------------------------------
        '''
        self.board = Board(10, 10)
        self.message_box = TextBox(
            x=10,
            y=self.board.height + self.board.y + 10,
            width=WINDOW_WIDTH - 20,
            height=WINDOW_HEIGHT - self.board.y - self.board.height - 20,
            background_color=(128, 255, 185)
        )

        self.score_board = TextBox(
            x = self.board.x + self.board.width + 10,
            y = self.board.y,
            width= WINDOW_WIDTH - 30 - self.board.width,
            height=75,
            border_width=1
        )

        # game replay button
        btn_w = (WINDOW_WIDTH - 30 - self.board.width)//2
        btn_h = 50
        btn_x = self.board.x + self.board.width + 10
        btn_y = self.score_board.y + self.score_board.height + 10

        self.prev_btn = TextBox(
            x=btn_x,
            y=btn_y,
            width=btn_w,
            height=btn_h,
            border_width=1,
            background_color=(87, 255, 129)
        )
        self.prev_btn.set_text("<=")

        self.next_btn = TextBox(
            x=btn_x + btn_w,
            y=btn_y,
            width=btn_w,
            height=btn_h,
            border_width=1,
            background_color=(87, 255, 129)
        )
        # self.next_btn.set_text("=>")
        next_icon = pygame.image.load(r"/home/tule/Pictures/next-button-icon.png")
        next_icon = pygame.transform.scale(
            next_icon,
            (min(self.next_btn.width, self.next_btn.height), min(self.next_btn.width, self.next_btn.height))
        )
        blit_surface_and_center(outer=self.next_btn.surface, inner=next_icon)
        # evaluate analyse
        self.eval_box = TextBox(
            x=btn_x,
            y=btn_y + btn_h*2 + 10,
            width=btn_w*2,
            height=btn_h,
            border_width=1,
            background_color=(87, 255, 129)
        )

        self.evaluation_bar = EvaluationBar(
            x=self.board.x + 10 + self.board.width,
            y=self.board.y,
            width=50,
            height=self.board.height,
            is_horizontal=False
        )



        self.exit_replay_mode_btn = TextBox(
            x=btn_x,
            y=btn_y + btn_h,
            width=btn_w*2,
            height=btn_h,
            border_width=1
        )

        self.exit_replay_mode_btn.set_text("exit review mode")

        self.components = [
            self.board,
            self.next_btn,
            self.message_box,
            self.score_board,
            self.eval_box,
            self.evaluation_bar
        ]

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
            self.match_record.append(move)
        except Exception as e:
            print(f"Can not put piece {self.next_turn} to position {move}")
            print(f"Exception message: {str(e)}")
            return

        if self.next_turn == X_PIECE:
            self.next_turn = O_PIECE
        else:
            self.next_turn = X_PIECE

        if self.eval_func is not None:
            self.eval_box.set_text(f"Evaluate: {self.eval_func(self.state, self.next_turn)}")
            x_, o_ = normalize_eval(self.eval_func(self.state, self.next_turn))
            self.evaluation_bar.set_evaluate(x_, o_)


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

    def game_replay(self):

        record_len = len(self.match_record)
        current_record = record_len -1
        self.message_box.set_text("Game replay mode")

        def display_board(n):
            gs = State()
            piece = [self.first_turn, O_PIECE if self.first_turn == X_PIECE else X_PIECE]
            for i in range(n+1):
                gs.execute_move(self.match_record[i], piece[i%2])
            self.board.set_state(gs)
            last_move = self.match_record[n]
            self.board.put_piece(
                row=last_move[0],
                col=last_move[1],
                piece=gs.cells[last_move[0]][last_move[1]],
                color= self.board.text_color_x if gs.cells[last_move[0]][last_move[1]] == X_PIECE else self.board.text_color_o,
                background=GREEN
            )

            if self.eval_func is not None:
                self.eval_box.set_text(f'evaluate: {self.eval_func(gs, piece[(n+1)%2])}')
                v = normalize_eval(self.eval_func(gs, piece[n%2]))
                self.evaluation_bar.set_evaluate(v[0], v[1])
        while True:
            # handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT:
                    mx, my = pygame.mouse.get_pos()
                    if self.prev_btn.contain_point(mx, my):
                        if current_record != 0:
                            current_record -= 1
                    elif self.next_btn.contain_point(mx, my):
                        if current_record != record_len-1:
                            current_record += 1
                    elif self.exit_replay_mode_btn.contain_point(mx, my):
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if current_record != 0:
                            current_record -= 1
                    elif event.key == pygame.K_RIGHT:
                        if current_record != record_len-1:
                            current_record += 1
            # render
            display_board(current_record)

            self.screen.fill(WHITE)

            self.eval_box.render()
            self.board.render()
            self.next_btn.render()
            self.prev_btn.render()
            self.exit_replay_mode_btn.render()
            self.message_box.render()
            self.evaluation_bar.render()
            self.clock.tick(self.fps)
            pygame.display.update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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
        if len(self.match_record) != 0:
            r, c = self.match_record[-1]
            # print(f"last move {r}, {c}")
            self.board.put_piece(
                row=r,
                col=c,
                piece=self.state.cells[r][c],
                color= self.board.text_color_x if self.state.cells[r][c] == X_PIECE else self.board.text_color_o,
                background=(0, 255, 0)
            )

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
        if self.state.status() == NOT_FINISH:
            return
        self.game_replay()

