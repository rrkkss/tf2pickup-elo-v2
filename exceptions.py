class IdNotFoundException(Exception):
    """Raised when player ID couldn't be found"""

class EloCouldntBeCalculated(Exception):
    """Raised when player's new elo couldn't be calculated"""

class ScoreCouldntBeFound(Exception):
    """"Raised when a score from log's json couldn't be found"""

class CouldntImportPackages(Exception):
    """Raised when setup couldn't import package"""

class CouldntGetEtf2lNickname(Exception):
    """Raised when there is no data or the data can't be parsed from ETF2L's API"""