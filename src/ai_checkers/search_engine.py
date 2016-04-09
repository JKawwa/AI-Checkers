"""The module containing search engine classes.
"""

import copy

class CheckersSearchEngine:
    """The search engine class. Used to perform searches on states.
    
    .. todo:: Write up search algorithm.
    """
    
    def DFMiniMax(self,n,player): 
        '''n is the current state'''
        '''//return Utility of state n given that //Player is MIN or MAX'''
        if n.is_end_state():
            return n.get_utility_value() #Return terminal states utility #//(V is specified as part of game)
        #//Apply Player’s moves to get successor 
        childList = n.get_successors()
        if player == "Min":
            return min(map(self.DFMiniMax,childList, ["Max"]*len(childList)))
        else:
            return max(map(self.DFMiniMax,childList, ["Min"]*len(childList)))  #over c in ChildList
    
    def __init__(self):
        pass
        
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
 
    def __str__(self):
        return ("Max" if self.get_is_max() else "Min") + ":" + ("AI" if self.get_is_ai() else "Human");

class AIError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 
                   

