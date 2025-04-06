import chess as ch
from ai.minimax import find_best_move
import argparse

class CommandLineChess:

    #  initialize the command line chess game.
    #Can start with a custom board state for testing purposes.
    def __init__(self, initial_board=None, depth=3):
        self.board = ch.Board(initial_board) if initial_board else ch.Board()
        self.move_history = []
        self.game_over = False
        self.depth = depth

    def print_board(self):
        #Print the current board state in a readable format.
        print("\n" + str(self.board) + "\n")

    def print_move_history(self):
        #Print the move history.
        print("\nMove History:")
        for i, move in enumerate(self.move_history):
            print(f"{i+1}. {move}")

    def print_turn(self):
        #Print whose turn it is.
        print(f"\n{'White' if self.board.turn else 'Black'}'s turn")

    def print_game_state(self):
        #Print the current game state.
        self.print_board()
        self.print_turn()

        # Check for game end conditions
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            print(f"\nCheckmate! {winner} wins!")
            self.game_over = True
        elif self.board.is_stalemate():
            print("\nStalemate! Game ends in a draw.")
            self.game_over = True
        elif self.board.is_insufficient_material():
            print("\nDraw due to insufficient material.")
            self.game_over = True
        elif self.board.is_fivefold_repetition():
            print("\nDraw by fivefold repetition.")
            self.game_over = True
        elif self.board.is_seventyfive_moves():
            print("\nDraw by 75-move rule.")
            self.game_over = True
        elif self.board.is_check():
            print(f"\n{'White' if self.board.turn else 'Black'} is in check!")

    #Process a human move from UCI string.
    #Returns True if move was successful, False otherwise.
    def process_human_move(self, move_uci):
        try:
            move = ch.Move.from_uci(move_uci)

            # Check if move is legal
            if move in self.board.legal_moves:
                piece = self.board.piece_at(move.from_square)
                to_rank = ch.square_rank(move.to_square)

                # Handle pawn promotion
                if (piece and piece.piece_type == ch.PAWN and
                    ((piece.color == ch.WHITE and to_rank == 7) or
                     (piece.color == ch.BLACK and to_rank == 0)) and
                    not move.promotion):
                    # Default to queen promotion in command line for simplicity
                    move = ch.Move(move.from_square, move.to_square, promotion=ch.QUEEN)

                self.board.push(move)
                self.move_history.append(move_uci)
                return True
            return False
        except:
            return False

    # Process the AI move using the same minimax algorithm as the GUI version.
    def process_ai_move(self):
        print("\nAI is thinking...")
        ai_move = find_best_move(self.board, self.depth)

        # Handle pawn promotion (AI always promotes to queen)
        piece = self.board.piece_at(ai_move.from_square)
        if (piece and piece.piece_type == ch.PAWN and
            piece.color == ch.BLACK and ch.square_rank(ai_move.to_square) == 0):
            ai_move = ch.Move(ai_move.from_square, ai_move.to_square, promotion=ch.QUEEN)

        self.board.push(ai_move)
        self.move_history.append(ai_move.uci())
        print(f"AI plays: {ai_move.uci()}")

    # Run the main game loop for command line interaction.
    def run_game_loop(self):
        print("Command Line Chess Game")
        print("Enter moves in UCI format (e.g., 'e2e4' or 'e7e8q' for promotion)")
        print("Type 'exit' to quit the game\n")

        self.print_game_state()

        while not self.game_over:
            if self.board.turn == ch.WHITE:
                # White turn
                move_input = input("Your move: ").strip().lower()

                if move_input == 'exit':
                    print("Game exited by user.")
                    break

                if not self.process_human_move(move_input):
                    print("Invalid move. Try again.")
                    continue
            else:
                # Black turn
                self.process_ai_move()

            self.print_game_state()

#Test the game from a specific board position.
#fen_string: FEN notation of the starting position
#moves_to_test: List of moves to test (in UCI format)

def test_from_position(fen_string, moves_to_test=None, depth=3):
    print(f"\nStarting test from position:\n{fen_string}")
    game = CommandLineChess(fen_string, depth=depth)
    game.print_game_state()
    
    if moves_to_test:
        for move in moves_to_test:
            if game.board.turn == ch.WHITE:
                # Process test move
                print(f"\nTesting move: {move}")
                if game.process_human_move(move):
                    game.print_game_state()
                else:
                    print("Invalid test move!")
                    break
            else:
                # Let AI respond
                game.process_ai_move()
                game.print_game_state()
                
                if game.game_over:
                    break

# Start a normal game
parser = argparse.ArgumentParser(description="Play Command Line Chess with Minimax AI.")
parser.add_argument('--depth', type=int, default=3, help="Minimax search depth for the AI")
args = parser.parse_args()

#game = CommandLineChess()
#game.run_game_loop()
