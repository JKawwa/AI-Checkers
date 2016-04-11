"""
This module stores the configuration to be used.

"""

class Config(object):
    """
    The configuration singleton class to store configuration values.
    
    """
    
    #: int: The value of a promoted piece.
    KING_VAL = 2
    #: bool: Pushes AI decisions away from a stale-mate.
    AVOID_TIE= True
    #: int: Determines the depth to use for player 1 if it is an AI.
    P1_DEPTH = 2
    #: int: Determines the depth to use for player 2 if it is an AI.
    P2_DEPTH = 2
    #: str: Determines the algorithm to use for player 1 if it is an AI.
    P1_ALG = "MiniMax"
    #: int: Determines the algorithm to use for player 2 if it is an AI.
    P2_ALG = "AlphaBeta"
    #: bool: Flag for printing the metrics for the AI at the end of the game.
    PRINT_METRICS = True