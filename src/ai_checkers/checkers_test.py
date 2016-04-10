import unittest
import checkers_state
import search_engine

class AITestCase(unittest.TestCase):
    
    board_string =  (" 8   x   x   x   x\n"
                     " 7 x   x   x   x  \n"
                     " 6   x   x   x   x\n"
                     " 5                \n"
                     " 4                \n"
                     " 3 o   o   o   o  \n"
                     " 2   o   o   o   o\n"
                     " 1 o   o   o   o  \n"
                     "   A B C D E F G H\n")
    
    test_steps1 = ["A3-B4","D6-C5","B4-D6","E7-C5"]
    test_steps2 = ["A3-B4","B6-A5","B2-A3","C7-B6","A1-B2","D8-C7","G3-H4","F6-G5","H4-F6-D8"]
    
    test_minimax1_in = "A3-B4"
    
    def test_init(self):
        controller1 = search_engine.AIController()
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        self.assertEqual(str(board), AITestCase.board_string, "Board initialization failed!")
        self.assertEqual(board.get_player_turn(), True, "Player turn is incorrect")
        self.assertEqual(state.get_max_turn(), True, "Board turn does not match state turn")
        
    def test_successors(self):
        controller1 = search_engine.AIController()
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        childList = state.get_successors()
        self.assertEqual(len(childList),7,"Number of successors is incorrect.")
       
    def test_jump_successors(self):
        controller1 = search_engine.AIController()
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        childList = None
        for step in AITestCase.test_steps1:
            childList = state.get_successors()
            for c in childList:
                if c.get_action() == step:
                    state = c
            self.assertEqual(state.get_action(),step,"Expected successor not found!")
            
        self.assertTrue(childList is not None)
        self.assertEqual(len(childList),2,"Wrong number of successors!")
    
    def test_double_jump_successors(self):
        controller1 = search_engine.AIController()
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        childList = None
        for step in AITestCase.test_steps2:
            childList = state.get_successors()
            for c in childList:
                if c.get_action() == step:
                    state = c    
            self.assertEqual(state.get_action(),step,"Expected successor not found!")
            
        self.assertTrue(childList is not None)
        self.assertEqual(len(childList),1,"Wrong number of successors!")
        
    def test_minimax1(self):
        controller1 = search_engine.AIController(mode="MiniMax", max_depth=1)
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        result = controller1.play_move(state)
            
        self.assertTrue(result is not None)
        self.assertEqual(result.get_action(), AITestCase.test_minimax1_in, "Wrong state selected!")
        self.assertEqual(controller1.get_engine().get_num_explored(),7,"Wrong number of states explored!")
        
    def test_minimax2(self):
        controller1 = search_engine.AIController(mode="MiniMax", max_depth=2)
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        result = controller1.play_move(state)
            
        self.assertTrue(result is not None)
        self.assertEqual(result.get_action(), AITestCase.test_minimax1_in, "Wrong state selected!")
        # First two levels with the algorithm should give 7 * 8 states explored.
        self.assertEqual(controller1.get_engine().get_num_explored(),7*8,"Wrong number of states explored!")
        
    def test_alphabeta1(self):
        controller1 = search_engine.AIController(mode="AlphaBeta", max_depth=1)
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        result = controller1.play_move(state)
            
        self.assertTrue(result is not None)
        self.assertEqual(result.get_action(), AITestCase.test_minimax1_in, "Wrong state selected!")
        self.assertEqual(controller1.get_engine().get_num_explored(),7,"Wrong number of states explored!")
        
    def test_alphabeta2(self):
        controller1 = search_engine.AIController(mode="AlphaBeta", max_depth=2)
        controller2 = search_engine.AIController()
        board = checkers_state.Board(controller1, controller2)
        state = checkers_state.CheckersState(board=board)
        result = controller1.play_move(state)
            
        self.assertTrue(result is not None)
        self.assertEqual(result.get_action(), AITestCase.test_minimax1_in, "Wrong state selected!")
        # First two levels with the algorithm should prune off 36 from total of 7 * 8 available states.
        self.assertEqual(controller1.get_engine().get_num_explored(),20,"Wrong number of states explored!")
        
if __name__ == '__main__':
    unittest.main()