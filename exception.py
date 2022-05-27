class IdNotFoundException(Exception):
    """Raised when player ID is not found"""

class EloCouldntBeCalculated(Exception):
    """Raised when player's new elo couldn't be calculated"""