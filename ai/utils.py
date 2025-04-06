import chess as ch

def sort_moves(board, moves, is_maxing):
    moves = list(moves)
    sorted_moves = sorted(moves, key=lambda move: move_score(board, move), reverse=is_maxing)

    return sorted_moves

def move_score(board, move):
    score = 0

    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece:
            # Higher value for bigger captures
            score += piece_value(captured_piece.piece_type)

    if board.gives_check(move):
        score += 1  # Small bonus for giving check

    # Later: Add promotion bonuses, killer moves, history heuristics, etc.
    
    return score

def piece_value(piece_type):
    if piece_type == ch.PAWN:
        return 1
    elif piece_type == ch.KNIGHT or piece_type == ch.BISHOP:
        return 3
    elif piece_type == ch.ROOK:
        return 5
    elif piece_type == ch.QUEEN:
        return 9
    return 0

# Count pawns in same col
def count_doubled_pawns(pawns):
    files = [0] * 8
    for pawn in pawns:
        file_index = pawn % 8
        files[file_index] += 1

    doubled_count = sum(max(0, count - 1) for count in files)
    return doubled_count


# count pawns with no pawn next to them
def count_isolated_pawns(pawns):
    files = [0] * 8
    for pawn in pawns:
        file_index = pawn % 8
        files[file_index] += 1

    isolated_count = 0
    for i in range(8):
        if files[i] > 0:
            # Check if there are pawns on adjacent files
            has_neighbor = False
            if i > 0 and files[i-1] > 0:
                has_neighbor = True
            if i < 7 and files[i+1] > 0:
                has_neighbor = True

            if not has_neighbor:
                isolated_count += files[i]

    return isolated_count

# cound passed pawns
def count_passed_pawns(board, pawns, color):
    passed_count = 0
    enemy_color = not color
    enemy_pawns = list(board.pieces(ch.PAWN, enemy_color))

    for pawn in pawns:
        file_index = pawn % 8
        rank_index = pawn // 8

        is_passed = True

        # Direction of "ahead" depends on color
        ahead_ranks = range(rank_index - 1, -1, -1) if color == ch.WHITE else range(rank_index + 1, 8)

        # Check files: same file and adjacent files
        check_files = [f for f in range(max(0, file_index - 1), min(8, file_index + 2))]

        # Check for enemy pawns ahead on these files
        for r in ahead_ranks:
            for f in check_files:
                square = r * 8 + f
                if any(ep == square for ep in enemy_pawns):
                    is_passed = False
                    break
            if not is_passed:
                break

        if is_passed:
            # Value increases as pawn advances
            advance_bonus = rank_index if color == ch.BLACK else (7 - rank_index)
            passed_count += 1 + (advance_bonus * 0.1)

    return passed_count

