import time as t
import random as rd
import copy as cp

threshhold = 10

def get_board(value):
    return [[value for i in range(9)] for j in range(9)]

def parse_row_input(input: str):
    values = [int(v) if v.strip() != '' else 0 for v in input.split(',')]
    if len(values) != 9:
        raise Exception(f"parse_row_input: there are more then 9 values ({len(values)}) in: {input}")
    elif len([v for v in values if v not in range(10)]) > 0:
        raise Exception(f"parse_row_input: invalid values {[v for v in values if v not in range(10)]}")
    return values

def get_user_input(mock: bool = False):
    if mock:
        return [
            "0,0,0,0,8,0,0,5,0",
            "0,7,6,0,0,2,0,0,3",
            "8,4,0,0,1,3,0,0,0",

            "2,8,0,6,9,0,3,7,5",
            "0,0,0,4,7,0,0,1,0",
            "1,9,7,2,3,0,8,0,4",

            "0,1,8,0,0,0,5,2,0",
            "0,0,0,0,2,0,6,0,8",
            "6,0,0,0,0,7,0,0,0",
        ]

    input_rows = []
    print("type rows with comma separate values:\n")
    for i in range(9):
        input_result = input()
        input_rows.append(input_result)
    return input_rows


def parse_user_input(input_rows: list):
    return [parse_row_input(row) for row in input_rows]


def get_board_from_user(mock: bool = False) -> object:
    user_input = get_user_input(mock)
    board = parse_user_input(user_input)
    if not check_board(board):
        raise Exception('get_board_from_user: invalid board, there is an error')
    return board


def define_fixed(input_rows: list):
    fixed = get_board(False)
    for row_idx, row in enumerate(input_rows):
        for col_idx, n in enumerate(row):
            fixed[row_idx][col_idx] = True if n > 0 else False
    return fixed


def print_3(values: list):
    return f"{values[0]} {values[1]} {values[2]}"


def print_row(row: list):
    return f"{print_3(row[0:3])} | {print_3(row[3:6])} | {print_3(row[6:9])}"


def print_board(board: list):
    for idx, row in enumerate(board):
        print(print_row(row))
        if (idx + 1) % 3 == 0 and idx != 8:
            print("------+-------+------")


def count_and_validate(list_to_count: list):
    counts = [0 for i in range(9)]
    for e in list_to_count:
        if e != 0:
            counts[e - 1] = counts[e - 1] + 1
    # return True if not any(c > 1 for c in counts) else False
    return not any(c > 1 for c in counts)


def check_row(row_index: int, board: list):
    row = board[row_index]
    return count_and_validate(row)


def check_column(col_index: int, board: list):
    col = [board[row_index][col_index] for row_index, row in enumerate(board)]
    return count_and_validate(col)


def check_square(square_index: int, board: list):
    row_range = list(range((square_index // 3) * 3, (square_index // 3) * 3 + 3))
    col_range = list(range((square_index % 3) * 3, (square_index % 3) * 3 + 3))
    square = []
    for r in row_range:
        for c in col_range:
            square.append(board[r][c])
    return count_and_validate(square)


def check_board(board):
    for i in range(9):
        r = [check_row(i, board), check_column(i, board), check_square(i, board)]
        if not all(r):
            return False
    return True


def get_position(number: int):
    row = number // 9
    col = number % 9
    return row, col


def solved(board):
    all_numbers = []
    for row_index, row in enumerate(board):
        for col_index, n in enumerate(row):
            all_numbers.append(n)
    return 0 not in all_numbers and check_board(board)


def go_back(fixed, n):
    c = 1
    fix = True
    while fix:
        row, col = get_position(n - c)
        fix = fixed[row][col]
        if fix:
            c += 1
    return n - c - 1


def go_forward(fixed, n):
    c = 1
    fix = True
    while fix:
        row, col = get_position(n + c)
        fix = fixed[row][col]
        if fix:
            c += 1
    return n + c + 1


def algorithm_forward(board, fixed):
    start = t.time()
    n = 0
    while n < 81 and not solved(board):
        row, col = get_position(n)
        if not fixed[row][col]:
            board[row][col] = board[row][col] + 1
            if board[row][col] == 10:
                board[row][col] = 0
                n = go_back(fixed, n)
                if n + 1 not in range(81) or round(t.time() - start, 4) > threshhold:
                    raise Exception(f'algorithm_forward: unsolvable')
            elif not check_board(board):
                continue
        n += 1
    elapsed = round(t.time() - start, 4)
    return elapsed


def algorithm_backward(board, fixed):
    start = t.time()
    n = 80
    while n > -1 and not solved(board):
        row, col = get_position(n)
        if not fixed[row][col]:
            board[row][col] = board[row][col] + 1
            if board[row][col] == 10:
                board[row][col] = 0
                n = go_forward(fixed, n)
                if n - 1 not in range(81) or round(t.time() - start, 4) > threshhold:
                    raise Exception(f'algorithm_backward: unsolvable')
            elif not check_board(board):
                continue
        n -= 1
    elapsed = round(t.time() - start, 4)
    return elapsed

def get_input_and_solve(mock: bool = False):
    board = get_board_from_user(mock)
    print("solving board: ")
    print_board(board)
    fixed = define_fixed(board)
    elapsed = algorithm_forward(board, fixed)
    print(f"\nsolved in {elapsed}s: ")
    print_board(board)

def generate_random_board(number_count: int):
    board = get_board(0)
    while number_count > 0:
        position = rd.randint(0, 80)
        row, col = get_position(position)
        if board[row][col] != 0:
            continue

        number = rd.randint(1, 9)
        board[row][col] = number
        if not check_board(board):
            board[row][col] = 0
        else:
            number_count -= 1
    return board

def solve1(board: list):
    to_be_solved = cp.deepcopy(board)
    fixed = define_fixed(to_be_solved)
    elapsed = algorithm_forward(to_be_solved, fixed)
    return elapsed, to_be_solved

def solve2(board: list):
    to_be_solved = cp.deepcopy(board)
    fixed = define_fixed(to_be_solved)
    elapsed = algorithm_backward(to_be_solved, fixed)
    return elapsed, to_be_solved

def check_for_differences(b1: list, b2: list):
    for row in range(len(b1)):
        for col in range(len(b2)):
            if b1[row][col] != b2[row][col]:
                return False
    return True

def count_value(board: list, value: int):
    count = 0
    for row in board:
        for item in row:
            if item == value:
                count += 1
    return count

def generate_valid_random_board(number_count: int):
    board = get_board_from_user(True)
    remove_count = 81 - number_count
    while count_value(board, 0) < remove_count:
        position = rd.randint(0, 80)
        row, col = get_position(position)
        if board[row][col] == 0:
            continue
        else:
            board[row][col] = 0
    return board

def print_result(value):
    if value == None:
        return "u"
    elif value:
        return "1"
    elif not value:
        return "0"
    else:
        return "?"



