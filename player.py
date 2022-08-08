class player:
    def __init__(
        self, id, nick, eloNew, eloOld, eloDif, bonusElo, gamesCount, wins, loses, draws, redGames, redLoses, redWins, redDraws, bluGames, bluLoses, bluWins, bluDraws,
        scoutGames, scoutPlayTime, scoutDPM, scoutKPM, scoutKD, scoutKDA, scoutACC, scoutKills, scoutAssists, scoutDeaths,
        soldierGames, soldierPlayTime, soldierDPM, soldierKPM, soldierKD, soldierKDA, soldierAirshots, soldierKills, soldierAssists, soldierDeaths,
        demoGames, demoPlayTime, demoDPM, demoKPM, demoKD, demoKDA, demoAirshots, demoKills, demoAssists, demoDeaths,
        medicGames, medicPlayTime, medicDPM, medicKPM, medicKD, medicKDA, medicHeals, medicUbers, medicHPM, medicKills, medicAssists, medicDeaths
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

def createPlayer(id, nick):
    return player(id, nick, 1600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
