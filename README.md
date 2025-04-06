# KNTU4032_Chess-Game-Development-with-Minimax-AI
This project is a chess game implemented in Python using Minimax AI with α-β pruning. The game features an interactive GUI built with Pygame and integrates the python-chess library for move validation and game logic.



# How to run 

Simply Clone the repository and go to the repo directory.

```
git clone https://github.com/afarin461/KNTU4032_Chess-Game-Development-with-Minimax-AI/
cd KNTU4032_Chess-Game-Development-with-Minimax-AI/
```

create a virtual environment ( if necessary ) and run 

``` bash
pip install -r requirements.txt
```

run `gui.py` to run the game : 

``` bash
python gui.py
```


# GUI

The GUI is Implemented using pygame.

There is a sidebar that shows 

    - Game history with the 10 recent moves played
    - When AI is making decision
    - Final Outcome of game

Upon choosing a white piece the legal moves are displayed by a transparent yellow layer behind them and the selected piece will be blue.

when a king is in check it will have a transparent red highlight.

# CommandLine

It is basically the same thing as gui but without graphics to speed things up.

It is implemented using a class to make testing faster and more robust.

Is contained in `cmdln.py` and uses the same logic and mostly the same code as `gui.py`


# Test
`test.py` is a file that is basically a compiled list of all edge cases and middle and end game scenarios to test the AI against.

There are 20 testcases and all tests have passed.

# TODO

### Interface

- [x] Maybe A better color combo?
- [x] Render Pieces.
- [x] Sidebar 
    - [x] Game history
    - [x] AI thinking message
    - [x] Display message a Stalemate Checkmate and Draw positions.
- [x] add legal move highlight
- [x] add king is in check highlight
- [x] add pawn promotion
    - [x] pawn promotion window for player
    - [x] AI always promotes to queen
- [x] integration with AI
- [x] Create CommandLine Playability for testing purposes.
    - [x] create tests that make sure checkmate is prioritized against stalemate
    - [x] create tests for other edge case scenarios

- [ ] add game timer

--- 

### AI

- [x] minimax ai
    - [x] added alpha beta pruning

- [x] evaluation function for minimax
    - [x] material counting
    - [x] piece position
    - [x] center aware
    - [x] pawn structure
    - [x] double bishop
    - [x] king safety methods
    - [x] make check / checkmate more favorable than draw/stalemate.

