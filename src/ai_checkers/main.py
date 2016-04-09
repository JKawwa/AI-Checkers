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
    
#     #Get first successor up to depth d
#     curr = state
#     for i in range(15):
#         print("successors ", i)
#         for succ_state in curr.get_successors():
#             succ_state.print_state()
#             curr = succ_state
#             break

    #Get next (alphaBeta) successor up to depth d
    engine = search_engine.SearchEngine(state, "AlphaBeta", 4)
    #for i in range(2):
    print("AB successors ", 0)
    next_state = engine.getNextState()
    if next_state:
        next_state.print_state()
    else:
        #break
        pass
        
    print("Nodes explored: "+str(engine.get_num_explored()))
        
    #Get next (minimax) successor up to depth d
    engine = search_engine.SearchEngine(state, "MiniMax", 4)
    #for i in range(2):
    print("MM successors ", 0)
    next_state = engine.getNextState()
    if next_state:
        next_state.print_state()
    else:
        #break
        pass
        
    print("Nodes explored: "+str(engine.get_num_explored()))
