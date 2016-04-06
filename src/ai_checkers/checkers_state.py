"""The module containing Checkers related classes.
"""

import copy
import search_engine

class CheckersState(search_engine.TwoPlayerGameState):
    """A state class. Used to define a Checkers game state.
    
    Args:
        parent (Optional[CheckersState]): The predecessor state.
        player1 (Optional[CheckersPlayer]): The player that will start first (MAX).
        player2 (Optional[CheckersPlayer]): The player that will start second (MIN).
    
    .. note:: The state must be provided either a parent state, or player1 and player2.
    
    .. todo:: Implement base class methods.
    """
    def __init__(self,action="START",parent=None,player1=None,player2=None):
        
        super().__init__(action = action, parent = parent, player1 = player1, player2 = player2)
        
        if parent:
            parent_board = parent.get_board()
            self.__board = copy.copy(parent_board)
            
        else:
            self.__board = Board(player1,player2)
        
    def get_board(self):
        """Gets the :class:`Board` linked to the current CheckersState.
    
        Returns:
            Board: The board.
        """
        return self.__board
        
    def get_successors(self):
        """Generates a list of successors for the state.
    
        Returns:
            List[TwoPlayerGameState]: The successor states.
        """
        raise search_engine.AIError("Method not implemented!")
    
    def get_hashable_state(self):
        """Provides a hashable object that uniquely defines the state.
    
        Returns:
            hashable: A hashable object.
        """
        raise search_engine.AIError("Method not implemented!")
    
    def print_state(self):
        """Prints a string representation of the state.
        """
        raise search_engine.AIError("Method not implemented!")
    
    def get_utility_value(self):
        """Provides the utility value of the state.
    
        Returns:
            int: The utility value of the state.
        """
        raise search_engine.AIError("Method not implemented!") 
        
class Board:
    
    """A board class. Can be used to define the state.
    
    Args:
        controller1 (Optional[Controller]): The player that will start first (MAX).
        controller2 (Optional[Controller]): The player that will start second (MIN).
        board (Optional[Board]): The board to copy the state from.
    """
        
    def __init__(self, controller1=None, controller2=None, board=None):
        if board:
            self.__player1 = CheckersPlayer(board=self,player=board.get_player1())
            self.__player2 = CheckersPlayer(board=self,player=board.get_player2())
            self.__player_turn = board.get_player_turn()
            self.__board = []
            for x in range(8):
                row = []
                for y in range(8):
                    old_pos = board.get_pos(x,y)
                    old_piece = old_pos.get_piece()
                    if old_piece:
                        is_player_1 = old_piece in board.get_player1().get_pieces()
                        piece = Piece(player=self.__player1 if is_player_1 else self.__player2, piece=old_piece)
                        row.append(Position(self,x,y,piece))
                    else:
                        row.append(Position(self,x,y))
                self.__board.append(row)
        else:
            self.__player1 = CheckersPlayer(board=self,controller=controller1)
            self.__player2 = CheckersPlayer(board=self,controller=controller2)
            controller1.set_is_max(True)
            controller2.set_is_max(False)
            self.__player_turn = self.__player1
            self.__board = []
            for x in range(8):
                row = []
                for y in range(8):
                    if (x<=2) and ((x+y)%2 == 0):
                        piece = Piece(self.__player1)
                        row.append(Position(self,x,y,piece))
                    elif (x>=5) and ((x+y)%2 == 0):
                        piece = Piece(self.__player2)
                        row.append(Position(self,x,y,piece))
                    else:
                        row.append(Position(self,x,y))
                self.__board.append(row)

    def get_relevant_player(self,controller):
        """
        Gets the player relevant to the controller.
            
        Args:
            controller (Controller): The controller to check players against.
            
        Returns:
            CheckersPlayer: The relevant player.
        """
        return self.__player1 if self.__player1.get_controller() is controller else self.__player2
    
    def get_player1(self):
        """
        Gets player 1.
            
        Returns:
            CheckersPlayer: The board's player 1.
        """
        return self.__player1
    
    def get_player2(self):
        """
        Gets player 2.
            
        Returns:
            CheckersPlayer: The board's player 2.
        """
        return self.__player2
    
    def get_player_turn(self):
        """
        Gets the player's turn.
            
        Returns:
            bool: True if it's Player 1's turn, False otherwise.
        """
        return self.__player_turn
    
    def set_player_turn(self,player_turn):
        """
        Gets the player's turn.
            
        Args:
            player_turn (bool): Player's turn. True if it's Player 1's turn, False otherwise.
        """
        self.__player_turn = player_turn
    
    def get_utility_value(self):
        """
        Gets the utility value of the board.
            
        Returns:
            int: The utility value.
        """
        return self.player1.get_value() - self.player2.get_value()
        
    def is_end_state(self):
        """
        Gets a boolean representing whether the game has ended.

        Returns:
            bool: Whether the game has ended.
        """
        return not self.player1.pieces or not self.player2.pieces
    
    def get_pos(self,x,y):
        """
        Gets the :class:`.Position` at the given board indices.
        
        Args:
            x (int): The row index.
            y (int): The column index.
            
        Returns:
            Position: The position at the given board indices.
        """
        return self.__board[x][y]                
        
    def get_board(self):
        """
        Gets a copy of the board.
            
        Returns:
            List[List[Position]]: The board as a list of lists.
        """
        return self.__board
        
                    
    def print_board(self):
        """
        Prints the board onto the standard output.
        """
        print(str(self))
                    
    def __str__(self):
        final_str = ''
        for x in range(8,-1,-1):
            for y in range(9):
                if x == 0:
                    final_str += ' '+str(y) if (y>0) else '  '
                elif y == 0:
                    final_str += ' '+chr(ord('A')+(x-1))
                else:
                    final_str += ' '+str(self.get_pos(x-1,y-1))
            final_str += '\n'
        return final_str

class Position:
    """A position class. Used for define positions on the checkers board.
    
    Args:
        board (Board): The board that the position is in.
        x (int): The position's row index.
        y (int): The position's column index.
        piece (Optional[Piece]): The piece that's in the position.
    """
    def __init__(self,board,x,y,piece=None):
        self.__board = board
        self.__x = x
        self.__y = y
        self.__piece = None
        
        self.set_piece(piece)
        
    def get_piece(self):
        """
        Gets the piece inside the position, if any.
        
        Returns:
            Position: The piece inside the position.
        """
        return self.__piece
        
    def set_piece(self,piece):
        """
        Sets the piece of the :class:`.Position` to the given :class:`.Piece`.
        
        Args:
            piece (Piece): The piece to place at the position.
        """
        if piece and piece.get_position() is not self:
            piece.set_position(self)
        self.__piece = piece
        
    def __str__(self):
        return str(self.__piece) if (self.__piece) else " "
    
    def __repr__(self):
        return str(self)
    
class Piece:
    """A piece class. Used for define pieces on the checkers board.
    
    Args:
        player (CheckersPlayer): The player that the piece belongs to.
        position (Optional[Position]): The position that the piece is on.
        piece (Optional[Piece]): A piece to copy properties from.
    """
    
    def __init__(self,player,position = None,piece = None):
        self.__player = player
        self.__position = None
        if(piece):
            self.__is_king = piece.get_is_king();
        else:
            self.__is_king = False
        
        self.set_position(position)
        player.add_piece(self)
        
    def set_king(self):
        """
        Change the type of :class:`.Piece` to a king.
        """
        self.__is_king = True
        
    def get_is_king(self):
        """
        Gets the type of :class:`.Piece`.
        
        Returns:
            bool: True if king, False otherwise.
        """
        return self.__is_king
        
    def set_position(self,position):
        """
        Sets the position of the :class:`.Piece` to the given :class:`.Position`.
        
        Args:
            position (Position): The position to set the piece to.
        
        """
        if self.__position and self.__position is not position:
            self.__position.set_piece(None)
        
        self.position = position
        
        if self.__position:
            self.__position.set_piece(self)
            
    def get_position(self):
        """
        Returns the position the piece is on.
        
        Returns:
            Position: The position the piece is on.
        
        """
        return self.__position
        
    def get_value(self):
        """
        Gets the value of the piece.
            
        Returns:
            int: The piece's value.
            
        .. note:: The value of the piece is 2 if it is a king and 1 otherwise.
        """
        return 2 if (self.is_king) else 1
    
    def __str__(self):
        final_str = 'o' if self.__player is self.__player.get_board().get_player1() else 'x'
        if self.__is_king:
            final_str = final_str.upper()
        return final_str
    
class CheckersPlayer():
    """A Checkers player class. Used for both human and AI players.
    
    Args:
        controller (Optional[Controller]): The controller to link the player to.
        board (Optional[Board]): The board to link the player to.
        player (Optional[Player]): A player to copy properties from.
    """
    
    def __init__(self,controller=None,board = None,player = None):
        #super().__init__(is_ai = is_ai)
        self.__board = board
        if player:
            self.__controller = player.get_controller()
        else:
            self.__controller = controller
        self.__pieces = []
        
    def get_controller(self):
        """
        Gets the controller this player is linked to.
            
        Returns:
            Board: The controller the player is linked to.
        """
        return self.__controller
    
    def get_board(self):
        """
        Gets the board this player is linked to.
            
        Returns:
            Board: The board the player is linked to.
        """
        return self.__board
        
    def get_pieces(self):
        """
        Gets a copy of the player's pieces as :class:`.List`[:class:`.Piece`]
                    
        Returns:
            List[Piece]: A list of the player's pieces.
        """
        return list(self.__pieces)
        
    def add_piece(self,piece):
        """
        Adds a piece to the player

        Args:
            piece (Piece): The piece to add.  
        """
        self.__pieces.append(piece)
        
    def remove_piece(self,piece):
        """
        Removes a piece from the player

        Args:
            piece (Piece): The piece to add.
        """
        if piece in self.__pieces:
            self.__pieces.remove(piece)
        
    def get_value(self):
        """
        Gets the value of the player's pieces.
            
        Returns:
            int: The sum of the player's pieces' values.
        """
        sum = 0
        for piece in self.__pieces:
            sum += piece.getValue()
        return sum
    
# class HumanPlayer(CheckersPlayer):
#     def __init__(self):
#         super().__init__(is_ai = True)
#         
#     def play_move(self):
#         pass
#         #x = raw_input('What is your name?')
#         
# class AIPlayer(CheckersPlayer):
#     def __init__(self):
#         super().__init__(is_ai = False)
#         
#     def play_move(self):
#         raise search_engine.AIError("Method not implemented!")