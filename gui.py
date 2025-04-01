import pygame as pg
import chess as ch
import chess.engine as en
from game import process_move


# CONSTANTS 
W, H = 1000, 1000 # Width, Height
cell_size = W//8 # Cell Size

cur_cell = None # Current Cell

# pygame
pg.init()
scr = pg.display.set_mode((W,H)) # screen


# DRAW THE CHESS BOARD
def draw_board():
    for r in range(8):
        for c in range(8):
            color = pg.color.THECOLORS['white'] if (r%2)==(c%2) else pg.color.THECOLORS["azure4"]
            # CHECK COLORS
            #print(f"({r},{c})",color) 

            rect = pg.Rect(r*cell_size, c*cell_size, cell_size, cell_size)
            pg.draw.rect(scr, color, rect)


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

    # Render Pieces
    for cell in ch.SQUARES:
        piece = board.piece_at(cell)
        if piece:
            c, r = ch.square_file(cell), 7 - ch.square_rank(cell)
            piece_name = f"{'white' if piece.color == ch.WHITE else 'black'}-"+piece.symbol().lower()
            screen.blit(pieces[piece_name], (c * cell_size , r * cell_size ))


def main():
    global cur_cell
    is_running = True
    board = ch.Board() # Chess board
    while is_running:
        draw_board()
        draw_pieces(scr, board, cell_size)

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                is_running = False
            if ev.type == pg.MOUSEBUTTONDOWN: # Convert Click to cell here once a click is detected
                cell = click_to_cell(ev.pos)

                if cur_cell is None:
                    cur_cell = cell
                else:
                    move = ch.Move(cur_cell, cell)
                    process_move(board,move)

                    cur_cell = None # reset move
                print(board)

        pg.display.flip()


    pg.quit()

main()
