import chess as ch
from cmdln import CommandLineChess, test_from_position
import time

# Run a series of test positions to evaluate the AI's performance.
def run_tests():
    test_results = {"passed": 0, "failed": 0}
    start_time = time.time()

    # Test 1: Fool's Mate (should find checkmate in 1)
    print("\n=== Test 1: Fool's Mate (AI should find checkmate) ===")
    fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
    test_from_position(fen, ["g1f3"])

    # Test 2: Scholar's Mate (AI should prevent immediate mate)
    print("\n=== Test 2: Scholar's Mate (AI should defend) ===")
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 3 4"
    test_from_position(fen)

    # Test 3: Stalemate position (AI should avoid stalemate)
    print("\n=== Test 3: Stalemate (AI should avoid draw) ===")
    fen = "k7/8/8/8/8/8/6R1/7K b - - 0 1"
    test_from_position(fen)

    # Test 4: King and pawn endgame (AI should promote pawn)
    print("\n=== Test 4: Pawn Promotion (AI should promote) ===")
    fen = "8/5k2/8/8/8/8/4P3/4K3 b - - 0 1"
    test_from_position(fen, ["e2e4"])

    # Test 5: Defensive position (AI should find best defense)
    print("\n=== Test 5: Defensive Position ===")
    fen = "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 4 8"
    test_from_position(fen, ["c4f7"])

    # Test 6: Checkmate in 2 (AI should find mate)
    print("\n=== Test 6: Checkmate in 2 ===")
    fen = "5rk1/ppp2ppp/3p4/4n3/2B5/2P2Q2/PP3PPP/R5K1 b - - 0 1"
    test_from_position(fen)

    # Test 7: Complex middlegame (AI should find good move)
    print("\n=== Test 7: Complex Middlegame ===")
    fen = "r1bq1rk1/pp1n1ppp/2p1pn2/3p4/2PP4/2NBPN2/PPQ2PPP/R4RK1 b - - 0 9"
    test_from_position(fen)

    # Test 8: Rook endgame (AI should find winning plan)
    print("\n=== Test 8: Rook Endgame ===")
    fen = "5k2/8/8/8/8/8/4R3/4K3 b - - 0 1"
    test_from_position(fen)

    # Test 9: Opposite colored bishops (should recognize drawish nature)
    print("\n=== Test 9: Opposite Colored Bishops ===")
    fen = "8/5k2/3b4/8/8/3B4/5K2/8 w - - 0 1"
    test_from_position(fen)

    # Test 10: Perpetual check (AI should avoid repetition)
    print("\n=== Test 10: Perpetual Check ===")
    fen = "5k2/5q2/5Q2/8/8/8/5K2/8 b - - 0 1"
    test_from_position(fen, ["f6h8"])

    elapsed_time = time.time() - start_time
    print(f"\nAll tests completed in {elapsed_time:.2f} seconds")

# Run realistic test positions from actual games to evaluate AI performance.
def run_realistic_tests():
    test_results = {"passed": 0, "failed": 0}
    start_time = time.time()

    # Test 11: Sicilian Defense, Najdorf Variation (typical opening)
    print("\n=== Test 11: Sicilian Najdorf (Opening) ===")
    fen = "rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq - 0 6"
    test_from_position(fen, ["e7e5"])

    # Test 12: Queen's Gambit Declined (middlegame with pawn tension)
    print("\n=== Test 12: Queen's Gambit Middlegame ===")
    fen = "r1bq1rk1/pp1n1ppp/2p1pn2/3p4/2PP4/2NBPN2/PPQ2PPP/R3K2R b KQ - 1 9"
    test_from_position(fen)

    # Test 13: Ruy Lopez, Berlin Defense (endgame transition)
    print("\n=== Test 13: Ruy Lopez Berlin Endgame ===")
    fen = "r1bq1rk1/pppn1ppp/3p1n2/4p3/2BPP3/5N2/PPP2PPP/RNBQR1K1 b - - 1 9"
    test_from_position(fen, ["f6e4"])

    # Test 14: King's Indian Attack (imbalanced position)
    print("\n=== Test 14: King's Indian Attack ===")
    fen = "rnbq1rk1/ppp1bppp/4pn2/3p4/3P1B2/2NBP3/PPPQ1PPP/R3K1NR b KQ - 5 8"
    test_from_position(fen)

    # Test 15: Caro-Kann Defense (structural battle)
    print("\n=== Test 15: Caro-Kann Structure ===")
    fen = "rn1qkbnr/pp2pppp/2p5/3pPb2/3P4/5N2/PPP2PPP/RNBQKB1R w KQkq - 1 5"
    test_from_position(fen, ["f3e5"])

    # Test 16: French Defense, Winawer (complex pawn structure)
    print("\n=== Test 16: French Winawer ===")
    fen = "rnbqk2r/ppp2ppp/4pn2/3p4/1b1PP3/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 2 6"
    test_from_position(fen)

    # Test 17: Slav Defense (piece activity test)
    print("\n=== Test 17: Slav Defense Activity ===")
    fen = "rnbqkb1r/pp2pppp/2p2n2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 1 4"
    test_from_position(fen, ["e7e6"])

    # Test 18: Benoni Counterattack (dynamic position)
    print("\n=== Test 18: Benoni Counterplay ===")
    fen = "rnbqkb1r/pp1p1ppp/4pn2/2p5/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq c6 0 5"
    test_from_position(fen)

    # Test 19: Dutch Defense (kingside attack)
    print("\n=== Test 19: Dutch Defense Attack ===")
    fen = "rnbq1rk1/pppp1ppp/4pn2/8/2PP4/5NP1/PP2PP1P/RNBQKB1R b KQ - 0 5"
    test_from_position(fen, ["f6e4"])

    # Test 20: English Opening (positional play)
    print("\n=== Test 20: English Positional ===")
    fen = "r1bqkb1r/pp1p1ppp/2n1pn2/2p5/2P5/2N1PN2/PP1P1PPP/R1BQKB1R w KQkq - 2 5"
    test_from_position(fen)

    elapsed_time = time.time() - start_time
    print(f"\nAll realistic tests completed in {elapsed_time:.2f} seconds")


print("=== Running All Test Suites ===")
run_tests()
run_realistic_tests()
print("\n=== All Tests Completed ===")
