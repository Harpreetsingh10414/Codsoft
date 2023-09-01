import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, depth, maximizing_player, alpha, beta):
    if is_winner(board, 'X'):
        return -1
    if is_winner(board, 'O'):
        return 1
    if is_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'O'
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'X'
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for i, j in get_empty_cells(board):
        board[i][j] = 'O'
        eval = minimax(board, 0, False, alpha, beta)
        board[i][j] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)
    return best_move

def main():
    print("Welcome to Tic-Tac-Toe!")
    user_name = input("Enter your name: ")
    ai_name = "AI"

    board = [[' ' for _ in range(3)] for _ in range(3)]

    while True:
        print_board(board)
        row, col = map(int, input(f"{user_name}, enter your move (row and column, e.g., '0 0'): ").split())
        if board[row][col] == ' ':
            board[row][col] = 'X'
            if is_winner(board, 'X'):
                print_board(board)
                print(f"Congratulations, {user_name}! You win!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            best_move = get_best_move(board)
            board[best_move[0]][best_move[1]] = 'O'

            if is_winner(board, 'O'):
                print_board(board)
                print(f"{ai_name} wins! {user_name}, you lose.")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break

if __name__ == "__main__":
    main()
