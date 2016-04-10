"""The entry point to our project.

Example:
    You can run the code by using::

        $ python main.py

"""

import search_engine
import checkers_state
import ai_config

def play_game():
    """
    Plays the game.
    """
    print("Enter game mode number:")
    print("1 - AI vs. AI")
    print("2 - Human vs. AI")
    print("3 - Human vs. Human")
    is_AI_vs_AI = input()
    if is_AI_vs_AI == '1':
        controller1 = search_engine.AIController(max_depth=ai_config.Config.player1_ai_depth)
        controller2 = search_engine.AIController(max_depth=ai_config.Config.player2_ai_depth)
    if is_AI_vs_AI == '1':
        controller1 = search_engine.AIController(max_depth=ai_config.Config.player1_ai_depth)
        controller2 = search_engine.AIController(max_depth=ai_config.Config.player2_ai_depth)
    else:
        controller1 = search_engine.HumanController()
        controller2 = search_engine.HumanController()
    
    board=checkers_state.Board(controller1, controller2)
    state = checkers_state.CheckersState(board=board)
    
    state.get_board().print_board()
    
    current_controller = controller1
    while( not state.is_end_state()):
        print(str(current_controller)+"'s Turn.")
        state = current_controller.play_move(state)
        if state is None:
            print("Quitting...")
            return
        print(str(current_controller) + ": " + state.get_action())
        state.get_board().print_board()
        current_controller = controller1 if state.get_max_turn() else controller2
        #print("Nodes explored: "+str(engine.get_num_explored()))
    winner = state.get_winner()
    # Game is over
    print((str(winner) + " wins!") if winner else "It's a Tie!")

if __name__ == '__main__':
    play_game()

#     controller1 = search_engine.Controller(True)
#     controller2 = search_engine.Controller(False)
#     board = checkers_state.Board(controller1, controller2)
#     state = checkers_state.CheckersState(board=board)
#     
#     state.get_board().print_board()
    
#     #Get first successor up to depth d
#     curr = state
#     for i in range(15):
#         print("successors ", i)
#         successors = curr.get_successors()
#         for succ_state in successors:
#             succ_state.print_state()
#             curr = succ_state
#             break

#     #Get next (alphaBeta) successor up to depth d
#     engine = search_engine.SearchEngine(state, "AlphaBeta", 4)
#     next_state = engine.getNextState()
#     if next_state:
#         next_state.print_state()
#     else:
#         #break
#         pass
#         
#     print("Nodes explored: "+str(engine.get_num_explored()))
#         
#     #Get next (minimax) successor up to depth d
#     engine = search_engine.SearchEngine(state, "MiniMax", 4)
#     next_state = engine.getNextState()
#     if next_state:
#         next_state.print_state()
#     else:
#         #break
#         pass
#          
#     print("Nodes explored: "+str(engine.get_num_explored()))
