import pygame as pg
import chess as ch
import chess.engine as en
import time
from game import process_move
from game import check_endgame
from game import isKingCheck
from ai.minimax import find_best_move


# CONSTANTS 
W, H = 860, 640 # Width, Height
cell_size = H//8 # Cell Size
sidebar_size = W - H
cur_cell = None # Current Cell
depth = 3 # minimax depth

# pygame
pg.init()
scr = pg.display.set_mode((W,H)) # screen


# DRAW THE CHESS BOARD
def draw_board(highlight=[], king_check_cells=[], ai_highlight=[]):
    font_labels = pg.font.Font(None, 20)

    for r in range(8):
        for c in range(8):
            square = ch.square(r, 7-c)
            color = pg.color.THECOLORS['white'] if (r%2)==(c%2) else pg.color.THECOLORS["teal"]
            # CHECK COLORS
            #print(f"({r},{c})",color) 

            rect = pg.Rect(r*cell_size, c*cell_size, cell_size, cell_size)
            pg.draw.rect(scr, color, rect)

            # Draw file labels (a-h) at bottom
            if c == 7:
                label = font_labels.render(chr(ord('a') + r), True, pg.color.THECOLORS["black"])
                scr.blit(label, (r * cell_size + cell_size // 2 - 6, H - 15))

            # Draw rank labels (1-8) at left
            if r == 0:
                label = font_labels.render(str(8 - c), True, pg.color.THECOLORS["black"])
                scr.blit(label, (4, c * cell_size + cell_size // 2 - 10))

            # Debugging: Show grid coordinates
            #font = pg.font.Font(None, 20)
            #text = font.render(f"{c},{r}", True, (255, 0, 0))
            #scr.blit(text, rect.topleft)

    highlight_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)  # Enable transparency
    highlight_surf.fill((255, 255, 0, 120))  # transparent yellow

    selected_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)  # Enable transparency
    selected_surf.fill((120, 120, 255, 120))  # transparent blue
    if cur_cell:
        c, r = ch.square_file(cur_cell), 7 - ch.square_rank(cur_cell)
        scr.blit(selected_surf, (c * cell_size, r * cell_size))  # Overlay currently selected square

    # Draw transparent highlights
    for square in highlight:
        c, r = ch.square_file(square), 7 - ch.square_rank(square)
        scr.blit(highlight_surf, (c * cell_size, r * cell_size))  # Overlay highlight

    # Draw transparent highlights
    for square in highlight:
        c, r = ch.square_file(square), 7 - ch.square_rank(square)
        scr.blit(highlight_surf, (c * cell_size, r * cell_size))  # Overlay highlight

    # Highlight AI's move (in green)
    ai_highlight_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)
    ai_highlight_surf.fill((0, 255, 0, 120))  # Transparent green
    for square in ai_highlight:
        c, r = ch.square_file(square), 7 - ch.square_rank(square)
        scr.blit(ai_highlight_surf, (c * cell_size, r * cell_size))

    # Draw transparent red highlights for kings in check
    red_highlight_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)  # Transparent red
    red_highlight_surf.fill((255, 0, 0, 100))  # transparent red
    for cell in king_check_cells:
        c, r = ch.square_file(cell), 7 - ch.square_rank(cell)
        scr.blit(red_highlight_surf, (c * cell_size, r * cell_size))  # Overlay red highlight




    # Draw Sidebar
    sidebar = pg.Rect(H, 0, sidebar_size, H)
    pg.draw.rect(scr, pg.color.THECOLORS["gray"], sidebar)


def draw_sidebar(scr, board, move_hist):
    sidebar = pg.Rect(H, 0, sidebar_size, H)
    pg.draw.rect(scr, pg.color.THECOLORS["gray"], sidebar)

    # Draw Title
    title_surf = font.render("Move History", True, pg.color.THECOLORS["black"])
    scr.blit(title_surf, (H + 20, 20))
    
    black_color = pg.color.THECOLORS["black"]
    white_color = (100, 100, 100)  # soft gray tone
    # Display last 10 moves
    for i, (white_move, black_move) in enumerate(move_hist[-10:]):
        y_offset = 50 + (i * 30)
        move_number = font.render(f"{len(move_hist)-10+i+1 if len(move_hist) > 10 else i+1}.", True, pg.color.THECOLORS["black"])
        white_surf = font.render(f"{white_move}", True, white_color)
        black_surf = font.render(f"{black_move}", True, black_color)

        scr.blit(white_surf, (H + 50, y_offset))
        scr.blit(black_surf, (H + 130, y_offset))
        scr.blit(move_number, (H + 20, y_offset))

    #turn_indic = font.render(f"{"White" if board.turn else "Black"}'s Turn", True, pg.color.THECOLORS["black"])
    #scr.blit(turn_indic, (H + (sidebar_size // 2) - 50, H - 20))

# convert click to cell
def click_to_cell(coords): # coordinates as tuple
    x,y = coords
    c, r = x // cell_size, y // cell_size

    return ch.square(c, 7 - r) # Convert to chess notation


def draw_pieces(screen, board, cell_size):
    # Load Pieces
    pieces = {}
    for color in ["black", "white"]:
        for piece in ["bishop", "knight", "queen", "king", "pawn", "rook"]:
            if piece=="knight":
                name = f"{color}-{piece[1]}"
            else:
                name = f"{color}-{piece[0]}"

            filename = f"{color}-{piece}"
            pieces[name] = pg.image.load("assets/"+filename+".png")
            pieces[name] = pg.transform.smoothscale(pieces[name], (cell_size - 10, cell_size-10))

    # Render Pieces
    for cell in ch.SQUARES:
        piece = board.piece_at(cell)
        if piece:
            c, r = ch.square_file(cell), 7 - ch.square_rank(cell)
            piece_name = f"{'white' if piece.color == ch.WHITE else 'black'}-"+piece.symbol().lower()

            # Calculate position to center piece
            piece_x = (c * cell_size) + (cell_size - pieces[piece_name].get_width()) // 2
            piece_y = (r * cell_size) + (cell_size - pieces[piece_name].get_height()) // 2

            screen.blit(pieces[piece_name], (piece_x, piece_y))


def display_message(scr, mess, font_size=28, color="blue"):
    font = pg.font.Font(None, font_size)  # Default system font
    text_surface = font.render(mess, True, pg.color.THECOLORS[color])  # defaults to blue text for announcing sth
    text_rect = text_surface.get_rect(center=(H + sidebar_size // 2, H - (H//6))) # Somewhere below history in side bar space
    scr.blit(text_surface, text_rect)



def handle_promotion(board, move):

    # Check if a pawn move to the last rank
    piece = board.piece_at(move.from_square)

    # If not a pawn, return original move
    if piece is None or piece.piece_type != ch.PAWN:
        return move

    # Check if moving to last rank
    toRank = ch.square_rank(move.to_square)
    if (piece.color == ch.WHITE and toRank != 7) or (piece.color == ch.BLACK and toRank != 0):
        return move

    # Set up promotion selection window
    promotionWindow = pg.Surface((320, 100))
    promotionWindow.fill(pg.color.THECOLORS["lightgray"])

    # Load piece images for selection
    promotionPieces = {}
    pieceKinds = [ch.QUEEN, ch.ROOK, ch.BISHOP, ch.KNIGHT]
    pieceNames = ["queen", "rook", "bishop", "knight"]
    color = "white" if piece.color == ch.WHITE else "black"

    # Load and scale images
    for i, kind in enumerate(pieceNames):
        img = pg.image.load(f"assets/{color}-{kind}.png")
        img = pg.transform.smoothscale(img, (60, 60))
        promotionPieces[pieceKinds[i]] = img

    # Create selection buttons
    buttonW = 70 # Width of buttons
    buttons = []
    for i, kind in enumerate(pieceKinds):
        rect = pg.Rect(10 + i * (buttonW + 5), 20, buttonW, buttonW)
        buttons.append((rect, kind))

    # Display window to choose promotion from in the middle
    windowPosition = ((W - 500) // 2, (H - 100) // 2)

    #selection of what piece to promote to
    currentPieces = None
    while currentPieces is None:

        # Draw promotion window
        scr.blit(promotionWindow, windowPosition)

        # Draw text
        promotionFont = pg.font.Font(None, 20)
        text = promotionFont.render("Select promotion piece:", True, pg.color.THECOLORS["black"])
        scr.blit(text, (windowPosition[0] + 10, windowPosition[1] + 5))

        # Draw piece options
        for i, (rect, kind) in enumerate(buttons):
            # Draw button background
            pg.draw.rect(scr, pg.color.THECOLORS["white"],
                        (windowPosition[0] + rect.x, windowPosition[1] + rect.y, rect.width, rect.height))

            # Draw piece image
            img = promotionPieces[kind]
            imgPosition = (windowPosition[0] + rect.x + (rect.width - img.get_width()) // 2,
                       windowPosition[1] + rect.y + (rect.height - img.get_height()) // 2)
            scr.blit(img, imgPosition)

            # Draw border
            pg.draw.rect(scr, pg.color.THECOLORS["black"], 
                        (windowPosition[0] + rect.x, windowPosition[1] + rect.y, rect.width, rect.height), 2)

        # Update display
        pg.display.flip()

        # Handle events
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                return move  # Return original move if user quits

            if ev.type == pg.MOUSEBUTTONDOWN:
                mousePosition = (ev.pos[0] - windowPosition[0], ev.pos[1] - windowPosition[1])
                for rect, kind in buttons:
                    if rect.collidepoint(mousePosition):
                        currentPieces = kind
                        break

    # Create a new move with promotion
    return ch.Move(move.from_square, move.to_square, promotion=currentPieces)


def main():
    global cur_cell, font
    start_time = time.time()

    is_running = True
    board = ch.Board() # Chess board

    # history
    move_hist = []  # each element is a tuple (white_move, black_move)
    pending_white_move = None

    font = pg.font.Font(None, 24) # font
    highlight = []
    ai_move_highlight = []  # Highlight for AI moves

    while is_running:
        # Check if any king is in check
        king_check_cells = isKingCheck(board)

        draw_board(highlight, king_check_cells, ai_move_highlight)
        draw_pieces(scr, board, cell_size)
        draw_sidebar(scr,board, move_hist)

        # Check if checkmate, stalemate or draw
        if check_endgame(board, scr, display_message):
            pg.display.flip()  # Make sure message shows
            time.sleep(4)      # Pause to show message
            is_running = False
            continue           # Skip remaining loop steps

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                is_running = False

            if ev.type == pg.MOUSEBUTTONDOWN and board.turn and not board.is_game_over(): # Convert Click to cell here once a click is detected and is white's turn
                cell = click_to_cell(ev.pos)

                if cur_cell is None:
                    piece = board.piece_at(cell)
                    if piece and piece.color == board.turn: # Make sure it is the correct turn
                        cur_cell = cell
                        highlight = [move.to_square for move in board.legal_moves if move.from_square == cell]


                else:
                    move = ch.Move(cur_cell, cell)


                    # Check if this is a legal move
                    is_legal = False
                    for legal_move in board.legal_moves:
                        if legal_move.from_square == cur_cell and legal_move.to_square == cell:
                            is_legal = True
                            break

                    if is_legal:
                        # Check for promotion
                        piece = board.piece_at(cur_cell)
                        if piece and piece.piece_type == ch.PAWN:
                            to_rank = ch.square_rank(cell)
                            if (piece.color == ch.WHITE and to_rank == 7) or (piece.color == ch.BLACK and to_rank == 0):
                                move = handle_promotion(board, move)

                    if move in board.legal_moves:
                        board.push(move)
                        pending_white_move = move

                        # Check for promotion
                        if board.piece_at(cur_cell) and board.piece_at(cur_cell).piece_type == ch.PAWN:
                            move = handle_promotion(board, move)

                    else:
                        print("Invalid Move!!!! --------------- ")

                    cur_cell = None # reset move
                    highlight = []

        if not board.turn and not board.is_game_over(): # If AI turn, Move AI using minimax
            print("AI's Turn!---------")

            # GUI HUI TO SHOW AI IS THINKING , BECAUSE WHO WOULD HAVE THOUGHT AI TAKES TIMMME
            display_message(scr, "AI THINKING!", 22, "red")
            pg.display.flip()

            opp_move = find_best_move(board,depth)
            ai_move_highlight = [opp_move.from_square, opp_move.to_square]

            # Check if AI is promoting a pawn
            if board.piece_at(opp_move.from_square) and board.piece_at(opp_move.from_square).piece_type == ch.PAWN:
                to_rank = ch.square_rank(opp_move.to_square)
                if (board.piece_at(opp_move.from_square).color == ch.BLACK and to_rank == 0):
                    # AI always promotes to queen
                    opp_move = ch.Move(opp_move.from_square, opp_move.to_square, promotion=ch.QUEEN)

            board.push(opp_move)

            if pending_white_move is not None:
                move_hist.append((pending_white_move, opp_move))
                pending_white_move = None
            else:
                move_hist.append(("-"), opp_move)



        pg.display.flip()


    pg.quit()

main()
