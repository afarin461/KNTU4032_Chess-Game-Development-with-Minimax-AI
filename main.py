import pygame
import chess
import chess.polyglot

WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
GRAY = (119, 136, 153)
DARK_BROWN = (181, 136, 99)
LIGHT_BROWN = (240, 217, 181)
BLUE = (106, 195, 217)

def load_images():
    images = {}
    pieces = {
        'r': 'black-rook', 'n': 'black-knight', 'b': 'black-bishop', 'q': 'black-queen', 'k': 'black-king', 'p': 'black-pawn',
        'R': 'white-rook', 'N': 'white-knight', 'B': 'white-bishop', 'Q': 'white-queen', 'K': 'white-king', 'P': 'white-pawn'
    }
    for symbol, filename in pieces.items():
        images[symbol] = pygame.image.load(f"assets/{filename}.png")
        images[symbol] = pygame.transform.scale(images[symbol], (SQUARE_SIZE, SQUARE_SIZE))
    return images

def draw_board(screen):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, images):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - square // 8
            col = square % 8
            piece_symbol = piece.symbol()
            screen.blit(images[piece_symbol], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

def highlight_square(screen, square):
    if square is not None:
        row = 7 - square // 8
        col = square % 8
        pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def highlight_moves(screen, board, square):
    if square is None:
        return
    for move in board.legal_moves:
        if move.from_square == square:
            to_sq = move.to_square
            row = 7 - to_sq // 8
            col = to_sq % 8
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)



eval_piece = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate_board(board):
    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = eval_piece.get(piece.piece_type, 0)
            eval += value if piece.color == chess.WHITE else -value
    return eval

def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def process_move(board, move):
    if move in board.legal_moves:
        board.push(move)

def get_ai_move(board, depth=2):
    _, move = minimax(board, depth, maximizing = False)
    return move

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess with Minimax AI")
    clock = pygame.time.Clock()
    images = load_images()

    board = chess.Board()
    running = True
    selected_square = None

    while running:
        draw_board(screen)
        highlight_square(screen, selected_square)
        highlight_moves(screen, board, selected_square)
        draw_pieces(screen, board, images)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                square = get_square_under_mouse(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        process_move(board, move)
                        selected_square = None
                    else:
                        selected_square = None

        if board.turn == chess.BLACK and not board.is_game_over():
            pygame.time.wait(300)  # Delay for effect
            ai_move = get_ai_move(board, depth=2)
            if ai_move:
                board.push(ai_move)

        if board.is_game_over():
            result = "Draw"
            if board.is_checkmate():
                result = "Black wins" if board.turn == chess.WHITE else "White wins"
            font = pygame.font.SysFont(None, 48)
            text = font.render(result, True, (255, 0, 0))
            screen.blit(text, (WIDTH//3, HEIGHT//3))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

    pygame.quit()

main()