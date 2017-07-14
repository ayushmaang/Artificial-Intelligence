board = ["."] * 42
player = 'x'

SQUARE_WEIGHTS = [1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1,
                  1, 2, 3, 3, 2, 1]

def score(my_board):
    total = 0
    for i in range(len(my_board)):
        if my_board[i] == "x":
            total += SQUARE_WEIGHTS[i]
        elif my_board[i] == "o":
            total -= SQUARE_WEIGHTS[i]
    return total

def game_over(b):
    for move in range(len(b)):
        temp = b[move]
        boolean = temp.__eq__(".")
        if not temp.__eq__("."):
            if(terminal_state(move,b) is not None):
                return terminal_state(move,b)
    return None

def terminal_state(start_move, b):
    dirs = [1, -1, -7, 7, -8, 8, 6, -6]
    for dir in dirs:
        move = start_move
        current = b[move]
        count = 0
        while move < 42 and move >= 0 and b[move] is current and b[move] is not ".":
            count += 1
            move += dir
            if count is 4:
                return current
    return None


def is_legal(move):
    if board[move] is not '.':
        return False
    return True


def legal_moves():
    return [moves for moves in range(0,7) if is_legal(moves)]


def make_move(move, player):
    if not is_legal(move):
        return False
    column = move
    while (board[column + 7] == "."):
        column += 7
        if column >= 35:
            break

    board[column] = player
    return column

def make_move_actual(b,move,player):
    column = move
    while (b[column + 7] == "."):
        column += 7
        if column >= 35:
            break
    b[column]= player

    return b


def opponent(player):
    if player == 'x':
        return 'o'
    return 'x'


def display(b):
    for x in range(len(b)):
        print(b[x], end="")
        if (x + 1) % 7 == 0:
            print(" ")
    print('')

def minimax(player, maxDepth, currentDepth):
    if player == "x":
        return max_dfs(board, player, maxDepth, currentDepth)[1]
    else:
        return min_dfs(board, player, maxDepth, currentDepth)[1]

def max_dfs(board, player, maxDepth, currentDepth):
    move = -1
    game = game_over(board)
    if(game != None):
        if(game_over(board)=="x"):
            return 999, None
        if (game_over(board) == "o"):
            return -999, None
        if(game_over(board)=="Draw"):
            return 0, None
    if (currentDepth >= maxDepth):
        return score(board), None
    v = -1000

    moves = legal_moves()

    for m in moves:
        board_copy = board.copy()
        new_move = make_move_actual(board_copy,m,player)
        new_value = min_dfs(new_move, opponent(player), maxDepth, currentDepth + 1)[0]
        if new_value > v:
            v = new_value
            move = m
    return v, move

def min_dfs( board, player, maxDepth, currentDepth):
    move = -1
    game = game_over(board)
    if(game != None):
        cool = board.copy()
        if(game_over(board) == "x"):
            return 999, None
        if (game_over(board) == "o"):
            return -999, None
        if(game_over(board)=="Draw"):
            return 0, None
    if (currentDepth >= maxDepth):
        return score(board), None
    v = 1000
    moves = legal_moves()
    for m in moves:
        board_copy = board.copy()
        new_move = make_move_actual(board_copy,m,player)
        new_value = max_dfs(new_move, opponent(player), maxDepth, currentDepth + 1)[0]
        if new_value < v:
            v = new_value
            move = m
    return v, move

player = 'x'
display(board)
move = int(input("move:")) -1
move = make_move(move, player)
display(board)
while game_over(board) is None:
    player = opponent(player)
    if player is "x":
        move = int(input("move:")) -1
    else:
        move = minimax(player,5,0)
    while make_move(move,player) is False:
        move = int(input("move invalid:"))-1
    display(board)
    print('')

