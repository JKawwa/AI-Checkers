"""
This module stores the configuration to be used.

"""

class Config(object):
    """
    The configuration singleton class to store configuration values.
    
    """
    
    #: int: The value of a promoted piece.
    king_value = 2
    #: bool: Pushes AI decisions away from a stale-mate.
    avoid_stalemate = True
    #: int: Determines the depth to use for player 1 if it is an AI.
    player1_ai_depth = 3
    #: int: Determines the depth to use for player 2 if it is an AI.
    player2_ai_depth = 3
    #: bool: Flag for printing the metrics for the AI at the end of the game.
    print_metrics = True