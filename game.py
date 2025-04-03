def process_move(board,move, move_hist):
    if move in board.legal_moves:
        board.push(move)
        move_hist.append(move)

        if len(move_hist) > 10:
            move_hist.pop(0)
    else:
        print("Invalid Move!!!! ------------------- ")

