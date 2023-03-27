class Player:
    def __init__(
        self, id: str, nick: str, eloNew: float, eloOld: float, eloDif: float, bonusElo: float, 
        gamesCount: int, wins: int, loses: int, draws: int, 
        redGames: int, redLoses: int, redWins: int, redDraws: int, 
        bluGames: int, bluLoses: int, bluWins: int, bluDraws: int,
        scoutGames: int, scoutPlayTime: float, scoutDPM: float, scoutDMG: int, scoutDT: int, scoutDTM: float, scoutKPM: float, scoutKD: float, scoutKDA: float, scoutDAPD: float, scoutKills: int, scoutAssists: int, scoutDeaths: int, scoutHR: int, scoutCPC: int,
        soldierGames: int, soldierPlayTime: float, soldierDPM: float, soldierDMG: int, soldierDT: int, soldierDTM: float, soldierKPM: float, soldierKD: float, soldierKDA: float, soldierDAPD: float, soldierAirshots: int, soldierKills: int, soldierAssists: int, soldierDeaths: int, soldierHR: int,
        demoGames: int, demoPlayTime: float, demoDPM: float, demoDMG: int, demoDT: int, demoDTM: float, demoKPM: float, demoKD: float, demoKDA: float, demoDAPD: float, demoAirshots: int, demoKills: int, demoAssists: int, demoDeaths: int, demoHR: int,
        medicGames: int, medicPlayTime: float, medicDPM: float, medicDMG: int, medicDT: int, medicDTM: float, medicKPM: float, medicKD: float, medicKDA: float, medicHeals: int, medicUbers: int, medicUD: int, medicHPM: float, medicKills: int, medicAssists: int, medicDeaths: int

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
        self.scoutDMG = scoutDMG
        self.scoutDT = scoutDT
        self.scoutDTM = scoutDTM
        self.scoutKPM = scoutKPM
        self.scoutKD = scoutKD
        self.scoutKDA = scoutKDA
        self.scoutDAPD = scoutDAPD
        self.scoutKills = scoutKills
        self.scoutAssists = scoutAssists
        self.scoutDeaths = scoutDeaths
        self.scoutHR = scoutHR
        self.scoutCPC = scoutCPC

        self.soldierGames = soldierGames
        self.soldierPlayTime = soldierPlayTime
        self.soldierDPM = soldierDPM
        self.soldierDMG = soldierDMG
        self.soldierDT = soldierDT
        self.soldierDTM = soldierDTM
        self.soldierKPM = soldierKPM
        self.soldierKD = soldierKD
        self.soldierKDA = soldierKDA
        self.soldierDAPD = soldierDAPD
        self.soldierAirshots = soldierAirshots
        self.soldierKills = soldierKills
        self.soldierAssists = soldierAssists
        self.soldierDeaths = soldierDeaths
        self.soldierHR = soldierHR
        
        self.demoGames = demoGames
        self.demoPlayTime = demoPlayTime
        self.demoDPM = demoDPM
        self.demoDMG = demoDMG
        self.demoDT = demoDT
        self.demoDTM = demoDTM
        self.demoKPM = demoKPM
        self.demoKD = demoKD
        self.demoKDA = demoKDA
        self.demoDAPD = demoDAPD
        self.demoAirshots = demoAirshots
        self.demoKills = demoKills
        self.demoAssists = demoAssists
        self.demoDeaths = demoDeaths
        self.demoHR = demoHR

        self.medicGames = medicGames
        self.medicPlayTime = medicPlayTime
        self.medicDPM = medicDPM
        self.medicDMG = medicDMG
        self.medicDT = medicDT
        self.medicDTM = medicDTM
        self.medicKPM = medicKPM
        self.medicKD = medicKD
        self.medicKDA = medicKDA
        self.medicHeals = medicHeals
        self.medicUbers = medicUbers
        self.medicUD = medicUD
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
        0,      # scoutDMG
        0,      # scoutDT
        0,      # scoutDTM
        0,      # scoutKPM
        0,      # scoutKPD
        0,      # scoutKAPD
        0,      # scoutDAPD
        0,      # scoutKills
        0,      # scoutAssists
        0,      # scoutDeaths
        0,      # scoutHR
        0,      # scoutCPC
        
        0,      # soldierGames
        0,      # soldierDPM
        0,      # soldierDMG
        0,      # soldierDT
        0,      # soldierDTM
        0,      # soldierKPM
        0,      # soldierKPD
        0,      # soldierKAPD
        0,      # soldierDAPD
        0,      # soldierAirshots
        0,      # soldierKills
        0,      # soldierAssists
        0,      # soldierDeaths
        0,      # soldierHR
        
        0,      # demoGames
        0,      # demoPlayTime
        0,      # demoDPM
        0,      # demoDMG
        0,      # demoDT
        0,      # demoDTM
        0,      # demoKPM
        0,      # demoKPD
        0,      # demoKAPD
        0,      # demoAirshots
        0,      # demoKills
        0,      # demoAssists
        0,      # demoDeaths
        0,      # demoHR
        
        0,      # medicGames
        0,      # medicPlayTime
        0,      # medicDPM
        0,      # medicDMG
        0,      # medicDT
        0,      # medicDTM
        0,      # medicKPM
        0,      # medicKPD
        0,      # medicKAPD
        0,      # medicHeal
        0,      # medicUbers
        0,      # medicUD
        0,      # medicKills
        0,      # medicAssists
        0,      # medicDeaths
        0, 0, 0 # mismatched cba
    )
