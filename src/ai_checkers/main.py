"""The entry point to our project.

Example:
    You can run the code by using::

        $ python main.py

"""

import search_engine
import checkers_state

if __name__ == '__main__':
    controller1 = search_engine.Controller(True)
    controller2 = search_engine.Controller(False)
    state = checkers_state.CheckersState(board=checkers_state.Board(controller1, controller2))
    
    state.get_board().print_board()
    
    curr = state
    for i in range(15):
        print("successors ", i)
        for succ_state in curr.get_successors():
            succ_state.get_board().print_board()
            curr = succ_state
            break
    
    pass
