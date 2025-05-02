import pygame

from state import *

def get_center_position(outer_size:tuple[int, int], inner_size:tuple[int, int]):
    x, y = 0, 0
    if inner_size[0] < outer_size[0]:
        x = (outer_size[0] - inner_size[0])//2
    if inner_size[1] < outer_size[1]:
        y = (outer_size[1] - inner_size[1]) //2
    return x, y

def blit_surface_and_center(outer:pygame.Surface, inner:pygame.Surface):
    pos = get_center_position(outer_size=outer.get_size(), inner_size=inner.get_size())
    outer.blit(inner, pos)


class Component:
    def __init__(self, x:int, y:int, width:int, height:int, outer_surface:pygame.Surface=None):
        if height < 0:
            height = 0
        if width < 0:
            width = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))

        if outer_surface is None:
            outer_surface = pygame.display.get_surface()
        self.outer_surface = outer_surface

    def render(self):
        self.outer_surface.blit(self.surface, (self.x, self.y))

    def convert_coordinate(self, outer_x, outer_y)->tuple[int, int]:
        return outer_x - self.x, outer_y - self.y

    def contain_point(self, outer_x, outer_y):
        return (0 <= (outer_x - self.x) < self.width) and (0 <= (outer_y - self.y) < self.height)

class TextBox(Component):
    def __init__(self,
                 x:int, y:int, width:int, height:int,
                 outer_surface:pygame.Surface=None,
                 text_color:tuple[int, int, int]=(0, 0, 0),
                 background_color:tuple[int, int, int]=(0, 255, 255),
                 font:pygame.font.Font=None,
                 border_width:int=0,
                 border_color:tuple[int, int, int]=(0, 0, 0)
    ):
        super().__init__(x, y, width, height, outer_surface)
        self.background_color = background_color
        self.text_color = text_color
        if font is None:
            font = pygame.font.Font(None, 30)
        self.font = font
        self.border_width = border_width
        self.border_color = border_color
        self.set_text("")

    def set_text(self, text:str):
        self.surface.fill(self.background_color)
        if self.border_width > 0:
            pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), width=self.border_width)
        text_display = self.font.render(text, True, self.text_color)
        blit_surface_and_center(outer=self.surface, inner=text_display)

class EvaluationBar(Component):
    def __init__(self, x: int, y: int, width: int, height: int, is_horizontal:bool=True):
        super().__init__(x, y, width, height)
        self.is_horizontal = is_horizontal
        self.set_evaluate(0.5, 0.5)


    def set_evaluate(self, eval_x:float, eval_o:float):
        self.surface.fill((255, 255, 255))
        if eval_o == 0:
            eval_x = 1.0
        elif eval_x == 0:
            eval_o = 1.0
        else:
            eval_x, eval_o = eval_x/(eval_x+eval_o), eval_o/(eval_x+ eval_o)

        rect_x = [0, 0, self.width, self.height]
        rect_o = [0, 0, self.width, self.height]

        if self.is_horizontal:
            rect_x[2] = int(self.width*eval_x)

            rect_o[0] = rect_x[2]
            rect_o[2] = self.width - rect_x[2]
        else:
            rect_x[3] = int(self.height * eval_x)

            rect_o[1] = rect_x[3]
            rect_o[3] = self.height - rect_x[3]

        sur_x = pygame.Surface((rect_x[2], rect_x[3]))
        sur_x.fill(color=(255, 0, 0))
        # pygame.draw.rect(sur_x, (0, 0, 0), (0, 0, rect_x[2], rect_x[3]), width=1)

        sur_o = pygame.Surface((rect_o[2], rect_o[3]))
        sur_o.fill(color=(0,0,255))
        # pygame.draw.rect(sur_o, (0, 0, 0), (0, 0, rect_o[2], rect_o[3]), width=1)

        self.surface.blit(sur_x, (rect_x[0], rect_x[1]))
        self.surface.blit(sur_o, (rect_o[0], rect_o[1]))
        if self.is_horizontal:
            pygame.draw.line(
                self.surface,
                (0, 0, 0),
                start_pos=(self.width/2, 0),
                end_pos=(self.width/2, self.height)
            )
        else:
            pygame.draw.line(
                self.surface,
                (0, 0, 0),
                start_pos=(0, self.height/2),
                end_pos=(self.width, self.height/2)
            )



class Board(Component):
    _CELL_SIZE = 40
    def __init__(self,
                 x:int, y:int,
                 outer_surface:pygame.Surface=None,
                 font:pygame.font.Font=None,
                 background_color:tuple[int, int, int]=(255, 255, 255),
                 line_color:tuple[int, int, int]=(0, 0, 0),
                 text_color_x:tuple[int, int, int]=(255, 0, 0),
                 text_color_o:tuple[int, int, int]=(0, 0, 255)
    ):
        width = Board._CELL_SIZE * BOARD_SIZE
        height = Board._CELL_SIZE * BOARD_SIZE
        super().__init__(x, y, width, height, outer_surface)

        if font is None:
            font = pygame.font.Font(None, Board._CELL_SIZE - 5)

        self.font = font

        self.background_color = background_color
        self.line_color = line_color
        self.text_color_x = text_color_x
        self.text_color_o = text_color_o

        # mac dinh de trong
        self.set_state(State())
    def put_piece(self, row, col, piece, color, background):
        text_display = self.font.render(piece, True, color)

        pos = [col*Board._CELL_SIZE+1, row*Board._CELL_SIZE+1]
        # background
        cell = pygame.Surface((Board._CELL_SIZE-1, Board._CELL_SIZE-1))
        cell.fill(background)
        self.surface.blit(cell, pos)
        # text
        align = get_center_position((Board._CELL_SIZE, Board._CELL_SIZE), text_display.get_size())
        pos[0] += align[0]
        pos[1] += align[1]
        self.surface.blit(text_display, pos)
    def set_state(self, state:State):
        self.surface.fill(self.background_color)
        pygame.draw.rect(self.surface, self.line_color, (0, 0, self.width, self.height), width=2)
        for i in range(BOARD_SIZE - 1):
            w = 1
            if (i+1)%5 == 0:
                w = 2
            # duong ngang
            start = (0, (i + 1) * Board._CELL_SIZE)
            end = (Board._CELL_SIZE * BOARD_SIZE, (i + 1) * Board._CELL_SIZE)
            pygame.draw.line(self.surface, self.line_color, start, end, width=w)
            # duong doc
            start = ((i + 1) * Board._CELL_SIZE, 0)
            end = ((i + 1) * Board._CELL_SIZE, Board._CELL_SIZE * BOARD_SIZE)
            pygame.draw.line(self.surface, self.line_color, start, end, width=w)

        piece_x = self.font.render("X", True, self.text_color_x)
        piece_o = self.font.render("O", True, self.text_color_o)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if state.cells[row][col] != EMPTY_CELL:
                    piece = piece_x
                    if state.cells[row][col] == O_PIECE:
                        piece = piece_o
                    pos = [col*Board._CELL_SIZE, row*Board._CELL_SIZE]
                    align = get_center_position((Board._CELL_SIZE, Board._CELL_SIZE), inner_size=piece.get_size())
                    pos[0] += align[0]
                    pos[1] += align[1]
                    self.surface.blit(piece, pos)

    def mouse_click_at_cell(self, mx, my)->tuple[int, int]:
        coord= self.convert_coordinate(mx, my)
        return (coord[1]//Board._CELL_SIZE), (coord[0]//Board._CELL_SIZE)