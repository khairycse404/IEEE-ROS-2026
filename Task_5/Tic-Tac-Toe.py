def print_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(board, symbol):
    winning_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for case in winning_cases:
        if board[case[0]] == board[case[1]] == board[case[2]] == symbol:
            return True

    return False


def is_draw(board):
    for cell in board:
        if cell not in ["X", "O"]:
            return False
    return True


def get_valid_move(board):
    while True:
        move = input("Choose a position from 1 to 9: ")

        if not move.isdigit():
            print("Invalid input, Please enter a number")
            continue

        move = int(move)

        if move < 1 or move > 9:
            print("Invalid position, Choose from 1 to 9")
            continue

        index = move - 1

        if board[index] == "X" or board[index] == "O":
            print("This position is already taken, Choose another one")
            continue

        return index


def play_game():
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    print("Welcome to Tic-Tac-Toe")
    print_board(board)

    while True:
        player1_symbol = input("Player 1, choose your symbol X or O: ").upper()

        if player1_symbol == "X" or player1_symbol == "O":
            break
        else:
            print("Invalid symbol, Please choose X or O")

    if player1_symbol == "X":
        player2_symbol = "O"
    else:
        player2_symbol = "X"

    current_player = "Player 1"
    current_symbol = player1_symbol

    while True:
        print(f"{current_player}'s turn ({current_symbol})")

        move = get_valid_move(board)
        board[move] = current_symbol

        print_board(board)

        if check_winner(board, current_symbol):
            print(f"{current_player} wins")
            break

        if is_draw(board):
            print("Draw")
            break

        if current_player == "Player 1":
            current_player = "Player 2"
            current_symbol = player2_symbol
        else:
            current_player = "Player 1"
            current_symbol = player1_symbol


play_game()