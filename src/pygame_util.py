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
                 font:pygame.font.Font=None
    ):
        super().__init__(x, y, width, height, outer_surface)
        self.background_color = background_color
        self.text_color = text_color
        if font is None:
            font = pygame.font.Font(None, 30)
        self.font = font

        self.set_text("")

    def set_text(self, text:str):
        self.surface.fill(self.background_color)
        text_display = self.font.render(text, True, self.text_color)
        blit_surface_and_center(outer=self.surface, inner=text_display)

class Board(Component):
    _CELL_SIZE = 45
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