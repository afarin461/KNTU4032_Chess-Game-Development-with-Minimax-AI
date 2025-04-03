import pygame as pg
import chess as ch
import chess.engine as en
from game import process_move


# CONSTANTS 
W, H = 800, 600 # Width, Height
cell_size = H//8 # Cell Size
sidebar_size = W - H
cur_cell = None # Current Cell

# pygame
pg.init()
scr = pg.display.set_mode((W,H)) # screen


# DRAW THE CHESS BOARD
def draw_board(highlight=[]):
    for r in range(8):
        for c in range(8):
            square = ch.square(r, 7-c)
            color = pg.color.THECOLORS['white'] if (r%2)==(c%2) else pg.color.THECOLORS["teal"]
            # CHECK COLORS
            #print(f"({r},{c})",color) 

            rect = pg.Rect(r*cell_size, c*cell_size, cell_size, cell_size)
            pg.draw.rect(scr, color, rect)

            # Debugging: Show grid coordinates
            #font = pg.font.Font(None, 20)
            #text = font.render(f"{c},{r}", True, (255, 0, 0))
            #scr.blit(text, rect.topleft)

    highlight_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)  # Enable transparency
    highlight_surf.fill((255, 255, 0, 120))  # Yellow with 120 alpha (0 = fully transparent, 255 = solid)

    selected_surf = pg.Surface((cell_size, cell_size), pg.SRCALPHA)  # Enable transparency
    selected_surf.fill((120, 120, 255, 120))  # Yellow with 120 alpha (0 = fully transparent, 255 = solid)
    if cur_cell:
        c, r = ch.square_file(cur_cell), 7 - ch.square_rank(cur_cell)
        scr.blit(selected_surf, (c * cell_size, r * cell_size))  # Overlay currently selected square

    # Draw transparent highlights
    for square in highlight:
        c, r = ch.square_file(square), 7 - ch.square_rank(square)
        scr.blit(highlight_surf, (c * cell_size, r * cell_size))  # Overlay highlight



    # Draw Sidebar
    sidebar = pg.Rect(H, 0, sidebar_size, H)
    pg.draw.rect(scr, pg.color.THECOLORS["gray"], sidebar)


def draw_sidebar(scr, board, move_hist):
    sidebar = pg.Rect(H, 0, sidebar_size, H)
    pg.draw.rect(scr, pg.color.THECOLORS["gray"], sidebar)

    # Draw Title
    title_surf = font.render("Move History", True, pg.color.THECOLORS["black"])
    scr.blit(title_surf, (H + 20, 20))

    # Display last 10 moves
    for i, move in enumerate(move_hist[-10:]):
        move_surf = font.render(f"{i+1}. {move}", True, pg.color.THECOLORS["black"])
        scr.blit(move_surf, (H + 20, 50 + (i * 30)))

    turn_indic = font.render(f"{"White" if board.turn else "Black"}'s Turn", True, pg.color.THECOLORS["black"])
    scr.blit(turn_indic, (H + (sidebar_size // 2) - 50, H - 20))

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


def display_message(scr, mess, font_size=28):
    font = pg.font.Font(None, font_size)  # Default system font
    text_surface = font.render(mess, True, pg.color.THECOLORS["blue"])  # White text
    text_rect = text_surface.get_rect(center=(H + sidebar_size // 2, H - (H//6)))  # Center in sidebar
    scr.blit(text_surface, text_rect)

def main():
    global cur_cell, font
    is_running = True
    board = ch.Board() # Chess board

    # history
    move_hist = []
    font = pg.font.Font(None, 24) # font
    highlight = []
    while is_running:
        draw_board(highlight)
        draw_pieces(scr, board, cell_size)
        draw_sidebar(scr,board, move_hist)
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

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                is_running = False
            if ev.type == pg.MOUSEBUTTONDOWN: # Convert Click to cell here once a click is detected
                cell = click_to_cell(ev.pos)

                if cur_cell is None:
                    piece = board.piece_at(cell)
                    if piece and piece.color == board.turn: # Make sure it is the correct turn
                        cur_cell = cell
                        highlight = [move.to_square for move in board.legal_moves if move.from_square == cell]

                else:
                    move = ch.Move(cur_cell, cell)
                    process_move(board,move, move_hist)

                    cur_cell = None # reset move
                    highlight = []

                #print(board)

        pg.display.flip()


    pg.quit()

main()
