"""The module containing search engine classes.
"""

import copy

class SearchEngine:
    """The search engine class. Used to perform searches on states.
    
    .. todo:: Write up search algorithm.
    """
    
    def __init__(self,state=None,mode="AlphaBeta",max_depth=5):
        self.__state = state
        self.__max_depth = max_depth
        self.__mode = mode
        self.__explored = dict()
        self.__explored[state.get_hashable_state()] = state
        
    def getNextState(self):
        if self.__mode == "AlphaBeta":
            next_state = self.startAlphaBeta()
        else:
            next_state = self.startMiniMax()
        self.__state = next_state
        return next_state
    
    def set_state(self,state):
        self.__state = state
    
    def get_num_explored(self):
        return len(self.__explored.keys())
    
    def startMiniMax(self):
        
        is_max_turn = self.__state.get_max_turn()
        childList = self.__state.get_successors()
        
        choice = (None,float("-inf"))
        
        for c in childList:
            val = self.miniMax(c)
            if is_max_turn:
                if val > choice[1]:
                    choice = (c,val)
            else:
                if val < choice[1]:
                    choice = (c,val)
                
        print("Utility: "+str(choice[1]))
                
        return choice[0]
        
    def startAlphaBeta(self):
        alpha = float("-inf")
        beta = float("inf")
        
        is_max_turn = self.__state.get_max_turn()
        childList = self.__state.get_successors()
        
        choice = (None,float("-inf")) if is_max_turn else (None,float("inf"))
        
        for c in childList:
            val = self.alphaBeta(c,alpha,beta)
            if is_max_turn:
                if val > choice[1]:
                    choice = (c,val)
                    alpha = val
            else:
                if val < choice[1]:
                    choice = (c,val)
                    beta = val                
                
        print("Utility: "+str(choice[1]))
                
        return choice[0]
            
        
    def miniMax(self,state,depth=0): 
        """Gets the utility value of the given state.
        
        Args:
            state (TwoPlayerGameState): The predecessor state.
            limit (int): The maximum depth the algorithm should explore.
            depth (int): The current depth.
            
        Returns:
            float: The utility value of the state.
        
        """
        #self.__explored[state.get_hashable_state()] = state
        
        print("NextState (depth "+str(depth)+"):")
        
        if state in self.__explored.keys() or state.is_end_state() or depth >= self.__max_depth:
            return state.get_utility_value() #Return terminal state's utility value
        
        is_max_turn = state.get_max_turn()
        childList = state.get_successors()
        
        if is_max_turn:
            utility = float("-inf")
            for c in childList:
                utility = max(utility,self.miniMax(c, depth+1))
            return utility
        else:
            utility = float("inf")
            for c in childList:
                utility = min(utility,self.miniMax(c, depth+1))
            return utility
        
    def alphaBeta(self,state,alpha,beta,depth=0):
        """Gets the utility value of the given state, using alpha-beta pruning.
        
        Args:
            state (TwoPlayerGameState): The predecessor state.
            alpha (float): The current alpha value.
            beta (float): The current beta value.
            limit (int): The maximum depth the algorithm should explore.
            depth (int): The current depth.
        Returns:
            float: The utility value of the state.
        
        """
        #self.__explored[state.get_hashable_state()] = state
        
        print("NextState (depth "+str(depth)+"):")
        
        if state.is_end_state() or depth >= self.__max_depth:
            #Return terminal state's utility value
            return state.get_utility_value()
        
        is_max_turn = state.get_max_turn()
        childList = state.get_successors()
        
        if is_max_turn:
            for c in childList:
                if c in self.__explored.keys():
                    continue
                alpha = max(alpha, self.alphaBeta(c,alpha,beta,depth+1)) 
                if beta <= alpha:
                    break 
            return alpha
        else:
            for c in childList:
                if c in self.__explored.keys():
                    continue
                beta = min(beta, self.alphaBeta(c,alpha,beta,depth+1)) 
                if beta <= alpha:
                    break 
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
        else:
            self.__max_turn = True
            self.__controller1 = controller1
            self.__controller2 = controller2
        
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
        return self.__action

#     def get_current_player(self):
#         """
# 
#         Returns:
#             Player: the player who's turn it is
#         """
# 
#         return self.get_player1() if self.get_max_turn() else self.get_player2()
        
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

class Controller:
    """A controller class. Used for both human and AI players.
     
    Args:
        is_ai (Optional[bool]): Whether the controller is an AI player.
     
    """
     
    def __init__(self,is_ai=False):
#        self.__is_max = False
#         self.__board = board
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
        return ("Max" if self.get_is_max() else "Min") + ":" + ("AI" if self.get_is_ai() else "Human");

class AIError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 
                   
class HumanController(Controller):
    def __init__(self):
        print("NOTE: Moves should be inputed in the form (Current Piece Position - Desired Position), e.g. Enter'(F2-E3)' to move piece F2 to E3\n NOTE: For double moves, use (Current Piece Position - Intermediate Position - Final Position), e.g. Enter'(F2-D4-F6)' to move piece F2 to D4 to F6")
        super().__init__(is_ai = True)
         
    def play_move(self,state):
        '''Asks for the next move, checks if the move is valid, 
        Returns next state Or None to quit the game'''
        #Keep asking for the next move until a valid move.
        while(True):
            nextMove = input("What is your next move? e.g. Enter'(F2-E3)'\n Enter 'Quit' to exit")
            #Check if the move is valid
            if nextMove == 'Quit':
                return None
            childList = self.__state.get_successors()
            for c in childList:
                if c.get_action == nextMove:
                    return c
            # Move not possible    
            print("Invalid move!! Please try again...\n\n")
         
class AIController(Controller):
    """
    Utilizes AlphaBeta pruning to determine the next state
    """
    def __init__(self,mode="AlphaBeta",max_depth=5):
        self.__engine = SearchEngine(mode = mode, max_depth = max_depth)
        super().__init__(is_ai = False)
         
    def play_move(self,state):
        #Get next (alphaBeta) successor up to depth d
        
        #for i in range(2):
        self.__engine.set_state(state)
        return self.__engine.getNextState()

