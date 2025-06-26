import math


def check_winner(board, player):
    win_combos = [[0,1,2],[3,4,5],[6,7,8],
                  [0,3,6],[1,4,7],[2,5,8],
                  [0,4,8],[2,4,6]]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False


def minimax(board, depth, is_max):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if ' ' not in board:
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                best = max(best, minimax(board, depth + 1, False))
                board[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                best = min(best, minimax(board, depth + 1, True))
                board[i] = ' '
        return best


def ai_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = 'O'



def create_board():
    return [' ' for _ in range(9)]


def print_board(board):
    for i in range(3):
        print('|'.join(board[i*3:(i+1)*3]))
        if i < 2:
            print("-----")


def player_move(board):
    move = -1
    while move not in range(9) or board[move] != ' ':
        move = int(input("Choose your move (0–8): "))
    board[move] = 'X'



def play_game():
    board = create_board()
    print_board(board)
    while True:
        player_move(board)
        print_board(board)
        if check_winner(board, 'X'):
            print("You win!")
            break
        if ' ' not in board:
            print("It's a tie!")
            break

        ai_move(board)
        print("AI's move:")
        print_board(board)
        if check_winner(board, 'O'):
            print("AI wins!")
            break
        if ' ' not in board:
            print("It's a tie!")
            break

play_game()
