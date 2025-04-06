import chess as ch

def process_move(board,move, move_hist):
    if move in board.legal_moves:
        board.push(move)
        move_hist.append(move)

        if len(move_hist) > 10:
            move_hist.pop(0)
    else:
        print("Invalid Move!!!! ------------------- ")


def check_endgame(board, scr, display_message):
        if board.is_checkmate():
            display_message(scr, "Checkmate!")
        elif board.is_stalemate():
            display_message(scr, "Stalemate!")
        elif board.is_insufficient_material():
            display_message(scr, "Draw!")
        elif board.is_seventyfive_moves():
            display_message(scr, "Draw!")
        elif board.is_fivefold_repetition():
            display_message(scr, "Draw!")
        elif board.is_variant_draw():
            display_message(scr, "Draw!")


def isKingCheck(board):
    king_check_squares = []

    # Check if white king is in check
    if board.is_check() and board.turn == ch.WHITE:
        white_king_square = board.king(ch.WHITE)
        king_check_squares.append(white_king_square)

    # Check if black king is in check
    elif board.is_check() and board.turn == ch.BLACK:
        black_king_square = board.king(ch.BLACK)
        king_check_squares.append(black_king_square)

    return king_check_squares
