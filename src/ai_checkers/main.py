"""The entry point to our project.

Example:
    You can run the code by using::

        $ python main.py

"""

import search_engine
import checkers_state

if __name__ == '__main__':
    player1 = search_engine.Controller(True)
    player2 = search_engine.Controller(False)
    board = checkers_state.Board(player1, player2)
    board.print_board()
    pass