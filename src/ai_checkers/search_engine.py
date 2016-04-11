"""The module containing search engine classes.
"""

import ai_config
import time

class SearchEngine:
    """The search engine class. Used to perform searches on states.
    
    Args:
        state (Optional[TwoPlayerGameState]): The state to start with.
        max_depth (Optional[int]): The maximum depth to search.
        mode (Optional[str]): The algorithm to use. "MiniMax" for MiniMax algorithm and "AlphaBeta" for AlphaBeta algorithm.
    
    .. note:: The setting :attr:`.Config.avoid_stalemate` option allows for stale-mates to become unfavorable.
    
    """
    
    def __init__(self,state=None,mode="AlphaBeta",max_depth=5):
        self.__state = state
        self.__max_depth = max_depth
        self.__mode = mode
        self.__explored = dict()
        self.__time_elapsed = 0
#         if state:
#             self.__explored[state.get_hashable_state()] = state
        self.__num_explored = 0
        
    def getNextState(self):
        """
        Uses the set algorithm to find the most preferable next state.
        
        Returns:
            TwoPlayerGameState: The next state to be played.
        """
        if self.__mode == "AlphaBeta":
            next_state = self.startAlphaBeta()
        else:
            next_state = self.startMiniMax()
        self.__state = next_state
        return next_state
    
    def set_state(self,state):
        """
        Sets the state of the search engine.
        
        Args:
            state (TwoPlayerGameState): The state to be set.
        """
        self.__state = state
    
    def get_num_explored(self):
        """
        Gets the number of explored nodes from the last run.
        
        Returns:
            int: The number of explored nodes
        """
        return self.__num_explored
    
    def get_time_elapsed(self):
        """
        Gets the time elapsed for the last run.
        
        Returns:
            float: The time elapsed, in seconds
        """
        return self.__time_elapsed
    
    def startMiniMax(self):
        """
        Entry point for the MiniMax algorithm.
        Gives the most preferable next state.
        
        Returns:
            TwoPlayerGameState: The next state to be played.
        """
        start = time.time()
        
        is_max_turn = self.__state.get_max_turn()
        childList = self.__state.get_successors()
        
        if is_max_turn:
            choice = (None,float("-inf"))
        else:
            choice = (None,float("inf"))
        
        if(len(childList) == 1):
            choice = (childList[0],childList[0].get_utility_value())
        else:
            for c in childList:
                val = self.miniMax(c)
                if ai_config.Config.AVOID_TIE and c.check_path():
                        val = val + (-1 - val)/2
                if is_max_turn:
                    if val > choice[1]:
                        choice = (c,val)
                else:
                    if val < choice[1]:
                        choice = (c,val)
                
        self.__num_explored = len(self.__explored.keys())
        self.__explored.clear()
                
        end = time.time()
        
        self.__time_elapsed = end-start
        
        print("Utility: "+"{0:.3f}".format(choice[1]))
        print("Nodes Explored: "+str(self.__num_explored))
        print("Time Elapsed: "+"{0:.3f} seconds".format(self.__time_elapsed))
        
        return choice[0]
        
    def startAlphaBeta(self):
        """
        Entry point for the AlphaBeta pruning algorithm.
        Gives the most preferable next state.
        
        Returns:
            TwoPlayerGameState: The next state to be played.
        """
        start = time.time()
        
        alpha = float("-inf")
        beta = float("inf")
        
        is_max_turn = self.__state.get_max_turn()
        childList = self.__state.get_successors()
        
        choice = (None,float("-inf")) if is_max_turn else (None,float("inf"))
        
        if(len(childList) == 1):
            choice = (childList[0],childList[0].get_utility_value())
        else:
            for c in childList:
                val = self.alphaBeta(c,alpha,beta)
                if is_max_turn:
                    if ai_config.Config.AVOID_TIE and c.check_path():
                        val = val + (-1 - val)/2
                    if val > choice[1]:
                        choice = (c,val)
                        alpha = val
                else:
                    if ai_config.Config.AVOID_TIE and c.check_path():
                        val = val + (1 - val)/2
                    if val < choice[1]:
                        choice = (c,val)
                        beta = val                
                
        self.__num_explored = len(self.__explored.keys())
        self.__explored.clear()
        
        end = time.time()
        
        self.__time_elapsed = end-start
        
        print("Utility: "+"{0:.3f}".format(choice[1]))
        print("Nodes Explored: "+str(self.__num_explored))
        print("Time Elapsed: "+"{0:.3f} seconds".format(self.__time_elapsed))
        
        return choice[0]
            
        
    def miniMax(self,state,depth=0): 
        """Recursively gets the utility value of the given state.
        
        Args:
            state (TwoPlayerGameState): The predecessor state.
            depth (int): The current depth.
            
        Returns:
            float: The utility value of the state.
        
        """
        
        #print("NextState (depth "+str(depth)+"):")
        #print("Action: "+state.get_action())
        
        if state in self.__explored:
            return self.__explored[state.get_hashable_state()]
        
        if state.is_end_state() or depth >= (self.__max_depth - 1):
            self.__explored[state.get_hashable_state()] = state.get_utility_value()
            return state.get_utility_value() #Return terminal state's utility value
        
        is_max_turn = state.get_max_turn()
        childList = state.get_successors()
        
        if is_max_turn:
            utility = float("-inf")
            for c in childList:
                utility = max(utility,self.miniMax(c, depth+1))
            self.__explored[state.get_hashable_state()] = utility
            return utility
        else:
            utility = float("inf")
            for c in childList:
                utility = min(utility,self.miniMax(c, depth+1))
            self.__explored[state.get_hashable_state()] = utility
            return utility
        
    def alphaBeta(self,state,alpha,beta,depth=0):
        """Recursively gets the utility value of the given state, using alpha-beta pruning.
        
        Args:
            state (TwoPlayerGameState): The predecessor state.
            alpha (float): The current alpha value.
            beta (float): The current beta value.
            depth (int): The current depth.
        Returns:
            float: The utility value of the state.
        
        """
        
        #print("NextState (depth "+str(depth)+"):")
        #print("Action: "+state.get_action())
        if state in self.__explored:
            return self.__explored[state.get_hashable_state()]
        
        if state.is_end_state() or depth >= (self.__max_depth-1):
            #Return terminal state's utility value
            self.__explored[state.get_hashable_state()] = state.get_utility_value()
            return state.get_utility_value()
        
        is_max_turn = state.get_max_turn()
        childList = state.get_successors()
        
        if is_max_turn:
            for c in childList:
                #if c in self.__explored.keys():
                #    continue
                alpha = max(alpha, self.alphaBeta(c,alpha,beta,depth+1)) 
                if beta <= alpha:
                    break 
            self.__explored[state.get_hashable_state()] = alpha
            return alpha
        else:
            for c in childList:
                #if c in self.__explored.keys():
                #    continue
                beta = min(beta, self.alphaBeta(c,alpha,beta,depth+1)) 
                if beta <= alpha:
                    break 
            self.__explored[state.get_hashable_state()] = beta
            return beta
        
class TwoPlayerGameState:
    """A state class. Used to define a two-player game state.
    
    Args:
        parent (Optional[TwoPlayerGameState]): The predecessor state.
        player1 (Optional[Controller]): The player that will start first (MAX).
        player2 (Optional[Controller]): The player that will start second (MIN).
    
    .. note:: The state must be provided either a parent state, or player1 and player2.
    """
    
    def __init__(self,action="START",parent=None,controller1=None,controller2=None):
        if not (parent or (controller1 and controller2)):
            raise AIError("Must provide \"parent\" or (\"player1\" and \"player2\")")
        
        self.__action = action
        self.__parent = parent
        if parent:
            self.__max_turn = not parent.get_max_turn()
            # this is not desirable when we are removing pieces,
            # causes inconsistencies between board pieces & player pieces
            # Jad: The states are meant to have controllers that remain static between states.
            # Players get duplicated on each state, and then get connected to the controllers.
            self.__controller1 = parent.__controller1
            self.__controller2 = parent.__controller2
            self.__path = dict(parent.__path)
            self.__path[parent.get_hashable_state()] = parent
        else:
            self.__max_turn = True
            self.__controller1 = controller1
            self.__controller2 = controller2
            self.__path = dict()
        
    def get_controller1(self):
        """Gets the controller who starts first.
    
        Returns:
            Player: The controller who starts first.
        """
        return self.__controller1
    
    def get_controller2(self):
        """Gets the controller who starts second.
    
        Returns:
            Player: The controller who starts second.
        """
        return self.__controller2
        
    def get_max_turn(self):
        """Gets the player's turn.
    
        Returns:
            bool: True for player 1's turn, False
        """
        return self.__max_turn
    
    def get_parent(self):
        """Gets the state's parent.
    
        Returns:
            TwoPlayerGameState: The parent state.
        """
        return self.__parent
    
    def get_action(self):
        """Get's the state's action.
        
        Returns:
            str: The state's action.
        """
        return self.__action
    
    def set_action(self,action):
        """Sets the state's action.
        
        Args:
            action (str): The state's action.
        """
        self.__action = action

    def check_path(self):
        """Performs path checking
        
        Returns:
            bool: True if duplicate on path exists, false otherwise.
        """
        return self.get_hashable_state() in self.__path
#         node = self.get_parent()
#         while node:
#             if node.get_hashable_state() == self.get_hashable_state():
#                 return True
#             node = node.get_parent()
#         return False

    def get_successors(self):
        """Generates a list of successors for the state.
        **Must be implemented by child class**
    
        Returns:
            List[TwoPlayerGameState]: The successor states.
        """
        
        raise AIError("Must be implemented in child class!")  
    
    def get_hashable_state(self):
        """Provides a hashable object that uniquely defines the state.
        **Must be implemented by child class**
    
        Returns:
            hashable: A hashable object.
        """
        raise AIError("Must be implemented in child class!")  
    
    def print_state(self):
        """Prints a string representation of the state.
        **Must be implemented by child class**
        """
        raise AIError("Must be implemented in child class!")  
    
    def get_utility_value(self):
        """Provides the utility value of the state.
        **Must be implemented by child class**
    
        Returns:
            int: The utility value of the state.
        """
        raise AIError("Must be implemented in child class!")  

    def is_end_state(self):
        """Determines if the game has ended.
    
        Returns:
            bool: True if game ended. False otherwise.
        """
        return AIError("Must be implemented in child class!")
    
    def get_winner(self):
        """Retrieves the winner once the game has ended
    
        Returns:
            Controller: The winning controller. None otherwise.
        """
        return AIError("Must be implemented in child class!")

class Controller:
    """A controller class. Used for both human and AI players.
     
    Args:
        is_ai (Optional[bool]): Whether the controller is an AI player.
     
    """
     
    def __init__(self,is_ai=False):
        self.__is_ai = is_ai
 
    def get_is_ai(self):
        """
        Gets a boolean representing whether the controller is an AI or not (Human).
 
        Returns:
            bool: Whether the controller is a MAX Player.
        """
        return self.__is_ai
 
 
    def set_is_ai(self, is_ai):
        """
        Sets the controller as an AI or Human player
 
        Args:
            is_ai (bool): Whether the controller is an AI player.
        """
        self.__is_ai = is_ai
 
 
    def get_is_max(self):
        """
        Gets a boolean representing whether the controller is MAX or not (MIN).
 
        Returns:
            bool: Whether the player is a Max_Player.
        """
        return self.__is_max
 
 
    def set_is_max(self, is_max):
        """
        Sets the controller as a MAX or MIN player
 
        Args:
            is_max (bool): Whether the controller is a MAX Player.
        """
        self.__is_max = is_max
        
    def play_move(self,state):
        """
        Plays the controller's next move, based on the given state.
        
        Args:
            state (TwoPlayerGameState): The next state to be played.
        """
        raise AIError("Must be implemented for child class!")
 
    def __str__(self):
        return ("Player 1" if self.get_is_max() else "Player 2") + (" (AI)" if self.get_is_ai() else " (Human)");

class AIError(Exception):
    """
    The standard error to raise when an AI or game related exception occurs.
    
    Args:
        value (string): The error message.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 
                   
class HumanController(Controller):
    """
    The controller to be used by the user.
    """
    
    def __init__(self):
        print("NOTE: Moves should be inputed in the form (Current Piece Position - Desired Position), \ne.g. Enter'F2-E3' to move piece F2 to E3\nNOTE: For double moves, use (Current Piece Position - Intermediate Position - Final Position), \ne.g. Enter'F2-D4-F6' to move piece F2 to D4 to F6")
        super().__init__(is_ai = False)
         
    def play_move(self,state):
        """Asks for the next move, checks if the move is valid, 
        Returns:
            TwoPlayerGameState: Next state Or None to quit the game
        """
        #Keep asking for the next move until a valid move.
        while(True):
            childList = state.get_successors()
            print("Your possible moves:")
            i = 0
            for c in childList:
                if i > 0 and i%4 == 0:
                    print()
                print(c.get_action().ljust(10),end="\t");
                i += 1
            print()
            nextMove = input("What is your next move? \ne.g.'F2-E3' or 'Quit'\n")
            #Check if the move is valid
            if nextMove.lower() == 'Quit'.lower():
                return None
            for c in childList:
                if c.get_action().upper() == nextMove.upper():
                    return c
            # Move not possible    
            print("Invalid move!! Please try again...\n")
         
class AIController(Controller):
    """
    Utilizes AlphaBeta pruning to determine the next state
    """
    def __init__(self,mode="AlphaBeta",max_depth=5):
        super().__init__(is_ai = True)
        self.__engine = SearchEngine(mode = mode, max_depth = max_depth)
        self.average_time = 0 #: float: The average time taken to calculate the next step.
        self.average_nodes = 0  #: float: The average number of nodes explored.
        self.moves = 0 #: int: The number of moves played by this controller.
         
    def play_move(self,state):
        """"
        Gets the next successor using the defined algorithm up to depth d
            
        Returns:
            TwoPlayerGameState: The next state to be played.
        """
        self.__engine.set_state(state)
        result = self.__engine.getNextState()
        time_elapsed = self.__engine.get_time_elapsed()
        num_nodes = self.__engine.get_num_explored()
        if self.moves == 0:
            self.average_time = time_elapsed
            self.average_nodes = num_nodes
        else:
            self.average_time = ( (self.average_time * self.moves) + time_elapsed ) / (self.moves+1)
            self.average_nodes = ( (self.average_nodes * self.moves) + num_nodes ) / (self.moves+1)
        self.moves += 1
        return result
    
    def get_engine(self):
        """"
        Gets the :class:`SearchEngine` associated with the AIController.
            
        Returns:
            SearchEngine: The associated search engine.
        """
        return self.__engine

