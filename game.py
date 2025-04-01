def process_move(board,move):
    if move in board.legal_moves:
        board.push(move)
    else:
        print("Invalid Move!!!! ------------------- ")
