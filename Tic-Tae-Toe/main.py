import math
import tkinter as tk
from tkinter import messagebox

# Define the Tic-Tac-Toe board and other variables
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

player_turn = 'X'
ai_difficulty = 'Normal'

# Initialize the GUI
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create buttons for the Tic-Tac-Toe grid
buttons = [[None, None, None],
           [None, None, None],
           [None, None, None]]
def initialize_buttons():
    global buttons
    for i in range(3):
        button_row = []
        for j in range(3):
            button = tk.Button(root, text="", font=('normal', 30), width=6, height=2,
                               command=lambda row=i, col=j: on_button_click(row, col))
            button.grid(row=i, column=j)
            button_row.append(button)
        buttons.append(button_row)

initialize_buttons()

def start_new_game():
    global board, player_turn
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    player_turn = 'X'
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ""
            buttons[i][j]['state'] = 'normal'
    if ai_difficulty == 'AI - Hard':
        make_ai_move()

def is_game_over(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return True
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return True
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def evaluate_board(board):
    if any(row.count('O') == 3 for row in board) or \
       any(col.count('O') == 3 for col in zip(*board)) or \
       (board[0][0] == board[1][1] == board[2][2] == 'O') or \
       (board[0][2] == board[1][1] == board[2][0] == 'O'):
        return 1
    elif any(row.count('X') == 3 for row in board) or \
         any(col.count('X') == 3 for col in zip(*board)) or \
         (board[0][0] == board[1][1] == board[2][2] == 'X') or \
         (board[0][2] == board[1][1] == board[2][0] == 'X'):
        return -1
    else:
        return 0

def minimax(board, depth, maximizing_player, alpha, beta):
    if is_game_over(board) or depth == 0:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[i][j] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[i][j] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def make_ai_move():
    best_move = None
    best_eval = -math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                eval = minimax(board, depth=5, maximizing_player=False, alpha=-math.inf, beta=math.inf)
                board[i][j] = None
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    board[best_move[0]][best_move[1]] = 'O'
    buttons[best_move[0]][best_move[1]]['text'] = 'O'
    buttons[best_move[0]][best_move[1]]['state'] = 'disabled'
    if is_game_over(board):
        end_game()

def on_button_click(row, col):
    global player_turn
    if board[row][col] is None and player_turn == 'X':
        buttons[row][col]['text'] = 'X'
        board[row][col] = 'X'
        buttons[row][col]['state'] = 'disabled'
        if is_game_over(board):
            end_game()
        else:
            player_turn = 'O'
            make_ai_move()
            if is_game_over(board):
                end_game()

def end_game():
    result = evaluate_board(board)
    if result == 1:
        messagebox.showinfo("Game Over", "AI wins!")
    elif result == -1:
        messagebox.showinfo("Game Over", "Human wins!")
    else:
        messagebox.showinfo("Game Over", "It's a draw!")
    start_new_game()

def set_ai_difficulty(difficulty):
    global ai_difficulty
    ai_difficulty = difficulty
    start_new_game()

def reset_game():
    start_new_game()
    reset_button.pack_forget()

loading_label = tk.Label(root, text="Select Game Mode", font=('normal', 20))
loading_label.pack(pady=20)

human_button = tk.Button(root, text="Play against Human", font=('normal', 15), width=20,
                         command=lambda: set_ai_difficulty('Human'))
human_button.pack(pady=10)

normal_ai_button = tk.Button(root, text="Play against AI (Normal)", font=('normal', 15), width=20,
                             command=lambda: set_ai_difficulty('AI - Normal'))
normal_ai_button.pack(pady=10)

hard_ai_button = tk.Button(root, text="Play against AI (Hard)", font=('normal', 15), width=20,
                           command=lambda: set_ai_difficulty('AI - Hard'))
hard_ai_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset Game", font=('normal', 15), width=20, command=reset_game)

root.mainloop()
