from state import *


def find_chain(game_state:State, r:int, c:int, d:tuple[int, int])->tuple[int, int, int]:
    if game_state.cells[r][c] == EMPTY_CELL:
        return 0, 0, 0
    # huong nguoc lai
    d_ = (-d[0], -d[1])

    # quan hien tai
    piece = game_state.cells[r][c]

    # do dai chuoi
    left, mid, right = 0, 1, 0

    # tan cung ben trai(theo huong d_)
    p_left = [r, c]

    # tan cung ben phai(theo huong d)
    p_right = [r, c]

    # mid
    # di qua phai theo d
    for i in range(BOARD_SIZE):
        p_right[0] += d[0]
        p_right[1] += d[1]
        if not(0 <= p_right[0] < BOARD_SIZE and 0 <= p_right[1] < BOARD_SIZE) \
                or game_state.cells[p_right[0]][p_right[1]] != piece:
            p_right[0] -= d[0]
            p_right[1] -= d[1]
            break
        mid += 1

    # di qua trai theo d_
    for i in range(BOARD_SIZE):
        p_left[0] += d_[0]
        p_left[1] += d_[1]
        if not(0 <= p_left[0] < BOARD_SIZE and 0 <= p_left[1] < BOARD_SIZE) \
                or game_state.cells[p_left[0]][p_left[1]] != piece:
            p_left[0] -= d_[0]
            p_left[1] -= d_[1]
            break
        mid += 1

    # debug
    # print(f"piece{piece}")
    # print("p = ", r, c)
    # print("dir", d, d_)
    # print(f"bound: left-{p_left}, right-{p_right}")
    # right, d
    while right < WIN_LENGTH:
        p_right[0] += d[0]
        p_right[1] += d[1]
        if not(0 <= p_right[0] < BOARD_SIZE and 0 <= p_right[1] < BOARD_SIZE):
            break
        if game_state.cells[p_right[0]][p_right[1]] != piece and game_state.cells[p_right[0]][p_right[1]] != EMPTY_CELL:
            break
        right += 1

    #left, d_
    while left < WIN_LENGTH:
        p_left[0] += d_[0]
        p_left[1] += d_[1]
        if not (0 <= p_left[0] < BOARD_SIZE and 0 <= p_left[1] < BOARD_SIZE):
            break
        if game_state.cells[p_left[0]][p_left[1]] != piece and game_state.cells[p_left[0]][p_left[1]] != EMPTY_CELL:
            break
        left += 1

    return left, mid, right

def calc_chain_value(chain:tuple[int, int, int],  is_next_turn:bool)->int:
    if sum(chain) < WIN_LENGTH:
        return 0


    flag = 0
    # 1 left to win
    if chain[1] == WIN_LENGTH-1:
        if (chain[1] + chain[0] >= WIN_LENGTH) and (chain[1]+chain[2]) >= WIN_LENGTH:
            return 10**9 if is_next_turn else 10**8

        return 10**9 if is_next_turn else 10**5

    # 2 left to win
    if chain[1] == WIN_LENGTH-2:
        if (chain[1] + chain[0] >= WIN_LENGTH) and (chain[1] + chain[2]) >= WIN_LENGTH:
            return 10**7 if is_next_turn else 10**6
        return 10**4 if is_next_turn else 10*3

    # cac TH khac
    if (chain[1] + chain[0] >= WIN_LENGTH) and (chain[1] + chain[2]) >= WIN_LENGTH:
        return 100*chain[1]
    return 10*chain[1]


def calculate_at_point(game_state:State, r:int, c:int, next_turn:str)->int|float:
    valuate = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    is_next_turn = True if game_state.cells[r][c] == next_turn else False
    for d in directions:
        valuate += calc_chain_value(find_chain(game_state, r, c, d), is_next_turn)

    if game_state.cells[r][c] == O_PIECE:
        return -valuate
    return valuate

def evaluate_ver2(game_state:State, next_turn:str)->int|float:
    status = game_state.status()
    if status == X_WIN:
        # return 10**15
        return float('inf')
    elif status == O_WIN:
        # return -10**15
        return float('-inf')
    elif status == DRAW:
        return 0

    evaluate = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_state.cells[row][col] == EMPTY_CELL:
                continue
            evaluate += calculate_at_point(game_state, row, col, next_turn)
    return evaluate
