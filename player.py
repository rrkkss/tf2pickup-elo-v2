class Player:
    def __init__(
        self, id: str, nick: str, eloNew: float, eloOld: float, eloDif: float, bonusElo: float, 
        gamesCount: int, wins: int, loses: int, draws: int, 
        redGames: int, redLoses: int, redWins: int, redDraws: int, 
        bluGames: int, bluLoses: int, bluWins: int, bluDraws: int,
        scoutGames: int,    scoutPlayTime: float,   scoutDPM: int,      scoutKPM: float,    scoutKD: float,     scoutKDA: float,    scoutACC: float,        scoutKills: int,    scoutAssists: int,      scoutDeaths: int,
        soldierGames: int,  soldierPlayTime: float, soldierDPM: int,    soldierKPM: float,  soldierKD: float,   soldierKDA: float,  soldierAirshots: int,   soldierKills: int,  soldierAssists: int,    soldierDeaths: int,
        demoGames: int,     demoPlayTime: float,    demoDPM: int,       demoKPM: float,     demoKD: float,      demoKDA: float,     demoAirshots: int,      demoKills: int,     demoAssists: int,       demoDeaths: int,
        medicGames: int,    medicPlayTime: float,   medicDPM: int,      medicKPM: float,    medicKD: float,     medicKDA: float,    medicHeals: int,        medicUbers: int,    medicHPM: float,        medicKills: int, medicAssists: int, medicDeaths: int
    ):
        self.id = id
        self.nick = nick
        self.eloNew = eloNew
        self.eloOld = eloOld
        self.eloDif = eloDif
        self.bonusElo = bonusElo
        
        self.gamesCount = gamesCount
        self.wins = wins
        self.loses = loses
        self.draws = draws
        
        self.redGames = redGames
        self.redLoses = redLoses
        self.redWins = redWins
        self.redDraws = redDraws
        
        self.bluGames = bluGames
        self.bluLoses = bluLoses
        self.bluWins = bluWins
        self.bluDraws = bluDraws
        
        self.scoutGames = scoutGames
        self.scoutPlayTime = scoutPlayTime
        self.scoutDPM = scoutDPM
        self.scoutKPM = scoutKPM
        self.scoutKD = scoutKD
        self.scoutKDA = scoutKDA
        self.scoutACC = scoutACC
        self.scoutKills = scoutKills
        self.scoutAssists = scoutAssists
        self.scoutDeaths = scoutDeaths

        self.soldierGames = soldierGames
        self.soldierPlayTime = soldierPlayTime
        self.soldierDPM = soldierDPM
        self.soldierKPM = soldierKPM
        self.soldierKD = soldierKD
        self.soldierKDA = soldierKDA
        self.soldierAirshots = soldierAirshots
        self.soldierKills = soldierKills
        self.soldierAssists = soldierAssists
        self.soldierDeaths = soldierDeaths
        
        self.demoGames = demoGames
        self.demoPlayTime = demoPlayTime
        self.demoDPM = demoDPM
        self.demoKPM = demoKPM
        self.demoKD = demoKD
        self.demoKDA = demoKDA
        self.demoAirshots = demoAirshots
        self.demoKills = demoKills
        self.demoAssists = demoAssists
        self.demoDeaths = demoDeaths

        self.medicGames = medicGames
        self.medicPlayTime = medicPlayTime
        self.medicDPM = medicDPM
        self.medicKPM = medicKPM
        self.medicKD = medicKD
        self.medicKDA = medicKDA
        self.medicHeals = medicHeals
        self.medicUbers = medicUbers
        self.medicHPM = medicHPM
        self.medicKills = medicKills
        self.medicAssists = medicAssists
        self.medicDeaths = medicDeaths

def createPlayer(id: str, nick: str) -> Player:
    return Player(
        id, 
        nick, 
        1600,   # eloNew
        0,      # eloOld
        0,      # eloDif
        0,      # bonusElo
        0,      # gamesCount
        0,      # wins
        0,      # loses
        0,      # draws
        0,      # redGames
        0,      # redLoses
        0,      # redWins
        0,      # redDraws
        0,      # bluGames
        0,      # bluLoses
        0,      # bluWins
        0,      # bluDraws
        0,      # scoutGames
        0,      # scoutPlayTime
        0,      # scoutDPM
        0,      # scoutKPM
        0,      # scoutKD
        0,      # scoutKDA
        0,      # scoutACC
        0,      # scoutKills
        0,      # scoutAssists
        0,      # scoutDeaths
        0,      # soldierGames
        0,      # soldierPlayTime
        0,      # soldierDPM
        0,      # soldierKPM
        0,      # soldierKD
        0,      # soldierKDA
        0,      # soldierAirshots
        0,      # soldierKills
        0,      # soldierAssists
        0,      # soldierDeaths
        0,      # demoGames
        0,      # demoPlayTime
        0,      # demoDPM
        0,      # demoKPM
        0,      # demoKD
        0,      # demoKDA
        0,      # demoAirshots
        0,      # demoKills
        0,      # demoAssists
        0,      # demoDeaths
        0,      # medicGames
        0,      # medicPlayTime
        0,      # medicDPM
        0,      # medicKPM
        0,      # medicKD
        0,      # medicKDA
        0,      # medicHeals
        0,      # medicUbers
        0,      # medicHPM
        0,      # medicKills
        0,      # medicAssists
        0       # medicDeaths
    )
