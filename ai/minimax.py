import chess
from ai.evaluation import evaluate
from ai.utils import sort_moves

def find_best_move(board, depth):
    bestEval = float("-inf")
    finalMove = None
    alpha = float("-inf")
    beta = float("inf")

    moves_sorted = sort_moves(board, board.legal_moves, True)
    for move in moves_sorted:
        board.push(move)
        eval_val = minimax(board, depth-1, alpha, beta, False)[0]
        board.pop()

        if eval_val > bestEval:
            bestEval = eval_val
            finalMove = move

        alpha = max(alpha, eval_val)

    return finalMove

def minimax(board, depth, alpha, beta, is_maxing):
    if depth==0 or board.is_game_over():
        return evaluate(board),None

    finalMove = None

    if is_maxing:
        bestEval = float("-inf")

        moves_sorted = sort_moves(board, board.legal_moves, True)
        for move in moves_sorted:
            board.push(move)
            eval_val = minimax(board, depth-1,alpha, beta, False)[0]
            board.pop()

            if eval_val > bestEval:
                bestEval = eval_val
                finalMove = move

            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break

        return bestEval, finalMove

    else:
        minEval = float("inf")

        moves_sorted = sort_moves(board, board.legal_moves, True)
        for move in moves_sorted:
            board.push(move)
            eval_val = minimax(board, depth-1, alpha, beta, True)[0]
            board.pop()

            if eval_val < minEval:
                minEval = eval_val
                finalMove = move

            beta = min(beta, eval_val)
            if beta <= alpha:
                break

        return minEval, finalMove

