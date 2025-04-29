X_PIECE = 'X'
O_PIECE = 'O'
EMPTY_CELL = '.'

BOARD_SIZE = 10
WIN_LENGTH = 5

X_WIN = 0
O_WIN = 1
DRAW = 2
NOT_FINISH = 3

class State:
    def __init__(self):
        self.cells = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def __str__(self):
        s = ''
        for row in self.cells:
            s += '|' +  '|'.join(row) + '|\n'
        return s

    def get_empty_cells(self)->list[tuple[int, int]]:
        l = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.cells[row][col] == EMPTY_CELL:
                    l.append((row, col))
        return l

    def clone(self)->'State':
        new_state = State()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                new_state.cells[row][col] = self.cells[row][col]
        return new_state

    def reset(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.cells[row][col] = EMPTY_CELL


    def execute_move(self, position:tuple[int, int], piece:str):
        if not(piece == X_PIECE or piece == O_PIECE):
            raise RuntimeError("Invalid piece")
        if self.cells[position[0]][position[1]] != EMPTY_CELL:
            raise  RuntimeError("This position is not empty")
        self.cells[position[0]][position[1]] = piece

    def simulate_move(self, position:tuple[int, int], piece:str)->'State':
        next_state = self.clone()
        next_state.execute_move(position, piece)
        return next_state

    def status(self)->int:


        def check_line(r, c, direction):
            if self.cells[r][c] == EMPTY_CELL:
                return False
            piece = self.cells[r][c]
            for i in range(WIN_LENGTH):
                if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                    return False
                if self.cells[r][c] != piece:
                    return  False
                r += direction[0]
                c += direction[1]
            return True

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                for d in directions:
                    check = check_line(row, col, d)
                    if check:
                        if self.cells[row][col] == X_PIECE:
                            return X_WIN
                        return O_WIN

        if len(self.get_empty_cells()) == 0:
            return DRAW
        return NOT_FINISH