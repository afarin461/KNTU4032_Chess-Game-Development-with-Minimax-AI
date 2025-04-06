import chess
import chess.pgn
import time
import csv
import os
from ai.minimax import find_best_move

RESULTS_DIR = "self_play_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def simulate_game(depth_white, depth_black, game_id, flip_perspective=True):
    """
    Simulate a game with option to flip the board perspective.
    When flip_perspective is True, white's moves are calculated by flipping the board
    and finding the best move from black's perspective, then flipping back.
    """
    board = chess.Board()
    game = chess.pgn.Game()
    node = game
    game.headers["White"] = f"AI_Depth_{depth_white}"
    game.headers["Black"] = f"AI_Depth_{depth_black}"
    game.headers["Event"] = f"Self-play Simulation {game_id}"
    game.headers["Date"] = time.strftime("%Y.%m.%d")
    
    move_number = 1
    total_time = 0

    while not board.is_game_over():
        start = time.time()
        
        if board.turn == chess.WHITE and flip_perspective:
            # For white's move, flip the board to use black's evaluation advantage
            board_copy = board.copy()
            board_copy.turn = chess.BLACK  # This doesn't actually flip the board
            
            # Get all legal moves from the original board
            legal_moves = list(board.legal_moves)
            
            # Find the best move from black's perspective for all white's legal moves
            best_score = float("-inf")
            best_move = None
            
            for move in legal_moves:
                board.push(move)
                # Evaluate from black's perspective (which is biased positively for black)
                board.turn = chess.BLACK  # Force evaluation from black's perspective
                score = -evaluate_position(board)  # Negate because we're looking from white's perspective
                board.turn = chess.WHITE  # Restore the correct turn
                board.pop()
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            move = best_move
        else:
            # Normal minimax for black's moves
            depth = depth_white if board.turn == chess.WHITE else depth_black
            move = find_best_move(board, depth)
        
        elapsed = time.time() - start
        total_time += elapsed

        if move is None:
            break

        board.push(move)
        node = node.add_variation(move)
        move_number += 1

    result = "1/2-1/2"  # Default to draw
    termination = "UNKNOWN"
    
    if board.is_game_over():
        outcome = board.outcome()
        if outcome:
            result = outcome.result()
            termination = outcome.termination.name

    game.headers["Result"] = result
    game.headers["Termination"] = termination
    game.headers["FlippedPerspective"] = "Yes" if flip_perspective else "No"

    # Save PGN file
    pgn_path = os.path.join(RESULTS_DIR, f"game_{game_id}.pgn")
    with open(pgn_path, "w") as pgn_file:
        print(game, file=pgn_file)

    return {
        "game_id": game_id,
        "white_depth": depth_white,
        "black_depth": depth_black,
        "flip_perspective": flip_perspective,
        "result": result,
        "termination": termination,
        "total_moves": board.fullmove_number,
        "total_time_sec": round(total_time, 2),
        "pgn_path": pgn_path,
    }

def evaluate_position(board):
    """
    This is a simple wrapper function that will evaluate the board position.
    We need this to evaluate white's moves from black's perspective.
    """
    # Make a one-ply minimax call just to get the evaluation
    temp_score, _ = minimax_one_ply(board, 0, float("-inf"), float("inf"), True)
    return temp_score

def minimax_one_ply(board, depth, alpha, beta, is_maxing):
    """
    A one-ply version of minimax just to get position evaluation.
    Imported from minimax.py but simplified to just get evaluation.
    """
    from ai.evaluation import evaluate
    return evaluate(board), None

def simulate_multiple_games():
    depth_settings = [
        (1, 1),
        (2, 2),
        (3, 3),
        (2, 3),
        (3, 2),
    ]

    results = []

    # First run: with flipped perspective for white
    for idx, (w_depth, b_depth) in enumerate(depth_settings, 1):
        print(f"\n=== Simulation {idx}: White depth {w_depth}, Black depth {b_depth} (Flipped Perspective) ===")
        result = simulate_game(w_depth, b_depth, idx, flip_perspective=True)
        results.append(result)
        print(f"Game saved to {result['pgn_path']}")
        print(f"Result: {result['result']} ({result['termination']})")
        print(f"Total moves: {result['total_moves']}, Total time: {result['total_time_sec']}s")
        print("=" * 50)

    # Second run: without flipped perspective (original behavior)
    for idx, (w_depth, b_depth) in enumerate(depth_settings, len(depth_settings) + 1):
        print(f"\n=== Simulation {idx}: White depth {w_depth}, Black depth {b_depth} (Original) ===")
        result = simulate_game(w_depth, b_depth, idx, flip_perspective=False)
        results.append(result)
        print(f"Game saved to {result['pgn_path']}")
        print(f"Result: {result['result']} ({result['termination']})")
        print(f"Total moves: {result['total_moves']}, Total time: {result['total_time_sec']}s")
        print("=" * 50)

    # Write results CSV
    csv_path = os.path.join(RESULTS_DIR, "results.csv")
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nAll results saved in {RESULTS_DIR}/")

if __name__ == "__main__":
    simulate_multiple_games()
