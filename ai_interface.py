from ai.minimax import find_best_move


DEPTH = 3

def get_move(board):
    return find_best_move(board, DEPTH)

