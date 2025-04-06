import chess as ch
from ai.utils import count_doubled_pawns
from ai.utils import count_isolated_pawns
from ai.utils import count_passed_pawns
from ai.utils import can_checkmate_in_one

material_values = {
    ch.PAWN: 1 * 0.2,
    ch.KNIGHT: 3 * 0.2,
    ch.BISHOP: 3.1 * 0.2,  # little more than the knight
    ch.ROOK: 5 * 0.2,
    ch.QUEEN: 9 * 0.2,
    ch.KING: 0 # don't evaluate the king 
}

center_cells = [ch.D4, ch.D5, ch.E4, ch.E5]

# Piece tables for positional eval
# Higher values are better ( since black is AI )
pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 5, 5, 5, 5, 5, 5, 5,
    1, 1, 2, 3, 3, 2, 1, 1,
    0, 0, 0, 4, 4, 0, 0, 0,
    0, 0, 0, 5, 5, 0, 0, 0,
    1, -1, -1, 2, 2, -1, -1, 1,
    1, 2, 2, -2, -2, 2, 2, 1,
    0, 0, 0, 0, 0, 0, 0, 0
]

knight_table = [
    -5, -4, -3, -3, -3, -3, -4, -5,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -3, 0, 1, 1.5, 1.5, 1, 0, -3,
    -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
    -3, 0, 1.5, 2, 2, 1.5, 0, -3,
    -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
    -4, -2, 0, 0.5, 0.5, 0, -2, -4,
    -5, -4, -3, -3, -3, -3, -4, -5
]

bishop_table = [
    -2, -1, -1, -1, -1, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 1, 1, 0.5, 0, -1,
    -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
    -1, 0, 1, 1, 1, 1, 0, -1,
    -1, 1, 1, 1, 1, 1, 1, -1,
    -1, 0.5, 0, 0, 0, 0, 0.5, -1,
    -2, -1, -1, -1, -1, -1, -1, -2
]

rook_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0.5, 1, 1, 1, 1, 1, 1, 0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    0, 0, 0, 0.5, 0.5, 0, 0, 0
]

queen_table = [
    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -1, 0, 0.5, 0, 0, 0, 0, -1,
    -2, -1, -1, -0.5, -0.5, -1, -1, -2
]

king_middlegame_table = [
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -2, -3, -3, -4, -4, -3, -3, -2,
    -1, -2, -2, -2, -2, -2, -2, -1,
    2, 2, 0, 0, 0, 0, 2, 2,
    2, 3, 1, 0, 0, 1, 3, 2
]

piece_tables = {
    ch.PAWN: pawn_table,
    ch.KNIGHT: knight_table,
    ch.BISHOP: bishop_table,
    ch.ROOK: rook_table,
    ch.QUEEN: queen_table,
    ch.KING: king_middlegame_table
}


# Some constant to help favor checkmate or mate over stalemate and draw
mateScore = 50
nearMate = 25
drawScore = -2 # penalty for draw

def evaluate(board):

     # Black wins
    if board.is_checkmate() and board.turn == ch.WHITE:
        return mateScore
    # White wins
    elif board.is_checkmate() and board.turn == ch.BLACK:
        return -mateScore
    # Stalemate/draw - generally bad for black
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves() or board.is_repetition():
        # In general, a draw is slightly favorable for white (human) vs AI 
        #give negative score to draws
        return drawScore

    # Check for mate in one possibilities
    if not board.is_game_over():
        # If black has checkmate in one, give a high score
        if can_checkmate_in_one(board, ch.BLACK):
            return nearMate
        # If white can checkmate in one, give a ver low score
        if can_checkmate_in_one(board, ch.WHITE):
            return -nearMate


    score = 0.0

    score += evaluate_material(board)
    score += evaluate_piecepos(board)
    score += evaluate_center(board)
    score += evaluate_bishop(board)
    score += evaluate_pawn_structure(board) * 0.2
    score += evaluate_mobility(board) * 0.2
    score += evaluate_king(board) * 0.2
    score += evaluate_check(board) * 0.5

    # Initiative bonus
    score += 5 if board.turn == ch.WHITE else -5

    return score


# Evaluate potential for creating check
def evaluate_check(board):
    score = 0.0

    # Store current turn
    original_turn = board.turn

    # Evaluate check by Black
    board.turn = ch.BLACK
    black_check_moves = sum(1 for move in board.legal_moves if board.gives_check(move))

    # Evaluate check threats by White (human)
    board.turn = ch.WHITE
    white_check_moves = sum(1 for move in board.legal_moves if board.gives_check(move))

    # Restore original turn
    board.turn = original_turn

    # Score based on checking potential
    check_score = (black_check_moves - white_check_moves) * 0.2
    score += check_score

    return score

# Eval score for material counting
def evaluate_material(board):
    score = 0

    # Material Count
    for cell in ch.SQUARES:
        piece = board.piece_at(cell)
        if piece != None:
            val = material_values[piece.piece_type]
            if piece.color == ch.BLACK:
                score += val
            else:
                score -= val

    return score



#Eval score for Piece Positions using tables
def evaluate_piecepos(board):
    score = 0

    # Piece positioning
    for cell in ch.SQUARES:
        piece = board.piece_at(cell)
        if piece is not None:
            # Get position value from piece-square table
            table = piece_tables[piece.piece_type]
            position_value = table[cell] * 0.1  # Scale down the position values

            # Mirror the square for white pieces (tables are from black's perspective)
            if piece.color == ch.WHITE:
                mirrored_cell = 7 - (cell // 8) * 8 + (cell % 8)
                position_value = table[mirrored_cell] * 0.1
                score -= position_value
            else:
                score += position_value

    return score


# Eval score for center in mind
def evaluate_center(board):
    score = 0.0

    for cell in center_cells:
        if board.piece_at(cell):
            piece = board.piece_at(cell)
            if piece.color == ch.BLACK:
                score += 0.1
            else:
                score -= 0.1

    return score

# Eval more or less bishops method
def evaluate_bishop(board):
    score = 0.0

    # Check if more than or two Bishops, This should put it in at advantage
    wBishops = len(board.pieces(ch.BISHOP, ch.WHITE))
    bBishops = len(board.pieces(ch.BISHOP, ch.BLACK))

    if wBishops >= 2:
        score -= 0.3
    if bBishops >= 2:
        score += 0.3


    return score

# Eval mobility ( # of legal moves) score
def evaluate_mobility(board):
    score = 0.0

    cur_turn = board.turn
    board.turn = ch.BLACK
    bMobility = len(list(board.legal_moves))
    board.turn = ch.WHITE
    wMobility = len(list(board.legal_moves))
    board.turn = cur_turn

    mobility_score = (bMobility - wMobility) * 0.1
    score += mobility_score

    return score

# Eval king safety method
def evaluate_king(board):
    score = 0.0

    # King Safety
    w_king_cell = board.king(ch.WHITE)
    b_king_cell = board.king(ch.BLACK)

    # King pawn shield evaluation
    w_king_safety = evaluate_king_safety(board, w_king_cell, ch.WHITE)
    b_king_safety = evaluate_king_safety(board, b_king_cell, ch.BLACK)

    # Negative for white safety (lower is better for black)
    score -= w_king_safety * 0.2
    # Positive for black safety
    score += b_king_safety * 0.2

    # Open files near kings
    w_king_file = w_king_cell % 8
    b_king_file = b_king_cell % 8

    w_king_open_files = count_open_files_near_king(board, w_king_file)
    b_king_open_files = count_open_files_near_king(board, b_king_file)

    # Penalize open files near kings (negative for white, positive for black)
    score += w_king_open_files * 0.3
    score -= b_king_open_files * 0.3

    # Check for direct attacks on king
    if board.is_check():
        if board.turn == ch.WHITE:
            score += 0.5  # Good for black if white king is in check
        else:
            score -= 0.5  # Bad for black if black king is in check


    return score

# Eval score for the safety of black king
def evaluate_king_safety(board, king_square, color):
    safety_score = 0
    king_file = king_square % 8
    king_rank = king_square // 8

    # Check for castling rights as a safety factor
    if color == ch.WHITE:
        if board.has_kingside_castling_rights(ch.WHITE):
            safety_score += 2 * 0.2
        if board.has_queenside_castling_rights(ch.WHITE):
            safety_score += 1 * 0.2
    else:
        if board.has_kingside_castling_rights(ch.BLACK):
            safety_score += 2 * 0.2
        if board.has_queenside_castling_rights(ch.BLACK):
            safety_score += 1 * 0.2

    # King in the corner is safer in middlegame
    if king_file in [0, 7] and king_rank in [0, 7]:
        safety_score += 1 * 0.2

    # Evaluate pawn shield
    pawn_shield_score = evaluate_pawn_shield(board, king_square, color)
    safety_score += pawn_shield_score

    # Check for pieces defending the king
    defending_pieces = count_defending_pieces(board, king_square, color)
    safety_score += defending_pieces * 0.1 # maybe could be more

    return safety_score


# eval score for pawn shield in front of king 
def evaluate_pawn_shield(board, king_square, color):
    shield_score = 0
    king_file = king_square % 8
    king_rank = king_square // 8

    # Define the area to check for pawns based on king position and color
    files_to_check = []
    ranks_to_check = []

    # Check files: king's file and adjacent files
    for f in range(max(0, king_file - 1), min(8, king_file + 2)):
        files_to_check.append(f)

    # Check ranks: 1-2 squares in front of king (direction depends on color)
    if color == ch.WHITE:
        for r in range(min(8, king_rank + 3))[king_rank + 1:]:
            ranks_to_check.append(r)
    else:
        for r in range(max(0, king_rank - 2), king_rank):
            ranks_to_check.append(r)

    # Check for friendly pawns in the shield area
    for f in files_to_check:
        for r in ranks_to_check:
            square = r * 8 + f
            piece = board.piece_at(square)
            if piece and piece.piece_type == ch.PAWN and piece.color == color:
                # Pawns directly in front of king are more valuable for the shield
                if f == king_file:
                    shield_score += 1.5
                else:
                    shield_score += 1

    return shield_score


# Eval score for defenting cells around kings
def count_defending_pieces(board, king_square, color):
    defending_count = 0
    king_file = king_square % 8
    king_rank = king_square // 8

    # Check cells next to the king
    for f in range(max(0, king_file - 1), min(8, king_file + 2)):
        for r in range(max(0, king_rank - 1), min(8, king_rank + 2)):
            square = r * 8 + f
            if square != king_square:  # Skip the king's square itself
                attackers = board.attackers(color, square)
                defending_count += len(attackers)

    return defending_count


# Cound open files close to king
def count_open_files_near_king(board, king_file):
    open_files_count = 0

    # Check king's file and adjacent files
    for f in range(max(0, king_file - 1), min(8, king_file + 2)):
        file_has_pawn = False

        # Check if there are any pawns in this file
        for r in range(8):
            square = r * 8 + f
            piece = board.piece_at(square)
            if piece and piece.piece_type == ch.PAWN:
                file_has_pawn = True
                break

        if not file_has_pawn:
            open_files_count += 1

    return open_files_count


# Eval score for entire pawn struct
def evaluate_pawn_structure(board):
    score = 0

    # Get pawns for each color
    white_pawns = list(board.pieces(ch.PAWN, ch.WHITE))
    black_pawns = list(board.pieces(ch.PAWN, ch.BLACK))

    # Evaluate doubled pawns (same file)
    w_doubled = count_doubled_pawns(white_pawns)
    b_doubled = count_doubled_pawns(black_pawns)
    # Doubled pawns are bad (negative for white, positive for black)
    score += w_doubled * 0.5
    score -= b_doubled * 0.5

    # Evaluate isolated pawns (no friendly pawns on adjacent files)
    w_isolated = count_isolated_pawns(white_pawns)
    b_isolated = count_isolated_pawns(black_pawns)
    # Isolated pawns are bad (negative for white, positive for black)
    score += w_isolated * 0.3
    score -= b_isolated * 0.3

    # Evaluate passed pawns (no enemy pawns ahead on same or adjacent files)
    w_passed = count_passed_pawns(board, white_pawns, ch.WHITE)
    b_passed = count_passed_pawns(board, black_pawns, ch.BLACK)
    # Passed pawns are good (positive for white, negative for black)
    score -= w_passed * 0.6
    score += b_passed * 0.6

    # Evaluate pawn chains
    w_chain = evaluate_pawn_chains(white_pawns, ch.WHITE)
    b_chain = evaluate_pawn_chains(black_pawns, ch.BLACK)
    # Pawn chains are good (positive for white, negative for black)
    score -= w_chain * 0.4
    score += b_chain * 0.4

    return score

# Eval score for pawns that protect other pawns
def evaluate_pawn_chains(pawns, color):
    chain_value = 0

    for pawn in pawns:
        file_index = pawn % 8
        rank_index = pawn // 8

        # Calculate potential protecting pawn positions
        if color == ch.WHITE:
            protector_squares = []
            if file_index > 0 and rank_index > 0:
                protector_squares.append((rank_index - 1) * 8 + (file_index - 1))  # Diagonal left
            if file_index < 7 and rank_index > 0:
                protector_squares.append((rank_index - 1) * 8 + (file_index + 1))  # Diagonal right
        else:  # BLACK
            protector_squares = []
            if file_index > 0 and rank_index < 7:
                protector_squares.append((rank_index + 1) * 8 + (file_index - 1))  # Diagonal left
            if file_index < 7 and rank_index < 7:
                protector_squares.append((rank_index + 1) * 8 + (file_index + 1))  # Diagonal right

        # Check if any of these squares have a friendly pawn
        for square in protector_squares:
            if square in pawns:
                chain_value += 1

    return chain_value
