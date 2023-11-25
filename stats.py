import general, player, exceptions, etf2l, config

predictionRight = 0; predictionFalse = 0
playerList = []

def set_stats(
    player: player.Player, playerClass: str, playerClassTime: int, playerTeam: str, scoreBlu: int, scoreRed: int,
    playerDPM: int, playerKPD: float, playerKAPD: float, playerDMG: int, playerDT: int, playerDTM: float, playerDAPD: float,
    playerHR: int, playerAirshots: int, playerKills: int, playerAssists: int, playerDeaths: int,
    playerHeal: int, playerUbers: int, playerUD: int, playerCPC: int, playerKPM: int
) -> player.Player:
    
    player.gamesCount += 1

    winning_team = general.get_winning_team(scoreRed, scoreBlu)
    if winning_team != 'draw':
        #if the player won
        if general.compare_string(winning_team, playerTeam):
            player.wins += 1
            if playerTeam == 'Blue':
                player.bluGames += 1
                player.bluWins += 1
            elif playerTeam == 'Red':
                player.redGames += 1
                player.redWins += 1
        
        #if the player lost
        else:
            player.loses += 1
            if playerTeam == 'Blue':
                player.bluGames += 1
                player.bluLoses += 1
            elif playerTeam == 'Red':
                player.redGames += 1
                player.redLoses += 1
    
    # if the player drew
    else:
        player.draws += 1
        if playerTeam == 'Blue':
            player.bluGames += 1
            player.bluDraws += 1
        elif playerTeam == 'Red':
            player.redGames += 1
            player.redDraws += 1

    if playerClass == 'scout':
        player.scoutGames += 1
        player.scoutPlayTime += playerClassTime
        player.scoutDPM += playerDPM
        player.scoutDMG += playerDMG
        player.scoutDT += playerDT
        player.scoutDTM += playerDTM
        player.scoutKPM += playerKPM
        player.scoutKD += playerKPD
        player.scoutKDA += playerKAPD
        player.scoutDAPD += playerDAPD
        player.scoutKills += playerKills
        player.scoutAssists += playerAssists
        player.scoutDeaths += playerDeaths
        player.scoutHR += playerHR
        player.scoutCPC += playerCPC

    elif playerClass == 'soldier':
        player.soldierGames += 1
        player.soldierPlayTime += playerClassTime
        player.soldierDPM += playerDPM
        player.soldierDMG += playerDMG
        player.soldierDT += playerDT
        player.soldierDTM += playerDTM
        player.soldierKPM += playerKPM
        player.soldierKD += playerKPD
        player.soldierKDA += playerKAPD
        player.soldierDAPD += playerDAPD
        player.soldierAirshots += playerAirshots
        player.soldierKills += playerKills
        player.soldierAssists += playerAssists
        player.soldierDeaths += playerDeaths
        player.soldierHR += playerHR

    elif playerClass == 'demoman':
        player.demoGames += 1
        player.demoPlayTime += playerClassTime
        player.demoDPM += playerDPM
        player.demoDMG += playerDMG
        player.demoDT += playerDT
        player.demoDTM += playerDTM
        player.demoKPM += playerKPM
        player.demoKD += playerKPD
        player.demoKDA += playerKAPD
        player.demoDAPD += playerDAPD
        player.demoAirshots += playerAirshots
        player.demoKills += playerKills
        player.demoAssists += playerAssists
        player.demoDeaths += playerDeaths
        player.demoHR += playerHR

    elif playerClass == 'medic':
        player.medicGames += 1
        player.medicPlayTime += playerClassTime
        player.medicDPM += playerDPM
        player.medicDMG += playerDMG
        player.medicDT += playerDT
        player.medicDTM += playerDTM
        player.medicKPM += playerKPM
        player.medicKD += playerKPD
        player.medicKDA += playerKAPD
        player.medicHeals += playerHeal
        player.medicUbers += playerUbers
        player.medicUD += playerUD
        player.medicKills += playerKills
        player.medicAssists += playerAssists
        player.medicDeaths += playerDeaths

    return player

def calculate_averages(player: player.Player) -> player.Player:
    if player.scoutGames == 0: player.scoutGames = 1
    if player.soldierGames == 0: player.soldierGames = 1
    if player.demoGames == 0: player.demoGames = 1
    if player.medicGames == 0: player.medicGames = 1
    if player.bluDraws == 0: player.bluDraws = 1
    if player.redDraws == 0: player.redDraws = 1

    player.scoutPlayTime = round(player.scoutPlayTime / 3600, 2) #in hours
    player.scoutDPM = round(player.scoutDPM / player.scoutGames, 2)
    player.scoutDMG = round(player.scoutDMG / player.scoutGames, 2)
    player.scoutDT = round(player.scoutDT / player.scoutGames, 2)
    player.scoutDTM = round(player.scoutDTM / player.scoutGames, 2)
    player.scoutKPM = round(player.scoutKPM / player.scoutGames, 2)
    player.scoutKD = round(player.scoutKD / player.scoutGames, 2)
    player.scoutKDA = round(player.scoutKDA / player.scoutGames, 2)
    player.scoutDAPD = round(player.scoutDAPD / player.scoutGames, 2)
    player.scoutKills = round(player.scoutKills / player.scoutGames, 2)
    player.scoutAssists = round(player.scoutAssists / player.scoutGames, 2)
    player.scoutDeaths = round(player.scoutDeaths / player.scoutGames, 2)
    player.scoutHR = round(player.scoutHR / player.scoutGames, 2)
    player.scoutCPC = round(player.scoutCPC / player.scoutGames, 2)

    player.soldierPlayTime = round(player.soldierPlayTime / 3600, 2)
    player.soldierDPM = round(player.soldierDPM / player.soldierGames, 2)
    player.soldierDMG = round(player.soldierDMG / player.soldierGames, 2)
    player.soldierDT = round(player.soldierDT / player.soldierGames, 2)
    player.soldierDTM = round(player.soldierDTM / player.soldierGames, 2)
    player.soldierKPM = round(player.soldierKPM / player.soldierGames, 2)
    player.soldierKD = round(player.soldierKD / player.soldierGames, 2)
    player.soldierKDA = round(player.soldierKDA / player.soldierGames, 2)
    player.soldierDAPD = round(player.soldierDAPD / player.soldierGames, 2)
    player.soldierAirshots = round(player.soldierAirshots / player.soldierGames, 2)
    player.soldierKills = round(player.soldierKills / player.soldierGames, 2)
    player.soldierAssists = round(player.soldierAssists / player.soldierGames, 2)
    player.soldierDeaths = round(player.soldierDeaths / player.soldierGames, 2)
    player.soldierHR = round(player.soldierHR / player.soldierGames, 2)

    player.demoPlayTime = round(player.demoPlayTime / 3600, 2)
    player.demoDPM = round(player.demoDPM / player.demoGames, 2)
    player.demoDMG = round(player.demoDMG / player.demoGames, 2)
    player.demoDT = round(player.demoDT / player.demoGames, 2)
    player.demoDTM = round(player.demoDTM / player.demoGames, 2)
    player.demoKPM = round(player.demoKPM / player.demoGames, 2)
    player.demoKD = round(player.demoKD / player.demoGames, 2)
    player.demoKDA = round(player.demoKDA / player.demoGames, 2)
    player.demoDAPD = round(player.demoDAPD / player.demoGames, 2)
    player.demoAirshots = round(player.demoAirshots / player.demoGames, 2)
    player.demoKills = round(player.demoKills / player.demoGames, 2)
    player.demoAssists = round(player.demoAssists / player.demoGames, 2)
    player.demoDeaths = round(player.demoDeaths / player.demoGames, 2)
    player.demoHR = round(player.demoHR / player.demoGames, 2)

    player.medicPlayTime = round(player.medicPlayTime / 3600, 2)
    player.medicDPM = round(player.medicDPM / player.medicGames, 2)
    player.medicDMG = round(player.medicDMG / player.medicGames, 2)
    player.medicDT = round(player.medicDT / player.medicGames, 2)
    player.medicDTM = round(player.medicDTM / player.medicGames, 2)
    player.medicKPM = round(player.medicKPM / player.medicGames, 2)
    player.medicKD = round(player.medicKD / player.medicGames, 2)
    player.medicKDA = round(player.medicKDA / player.medicGames, 2)
    player.medicHeals = round(player.medicHeals / player.medicGames, 2)
    player.medicUbers = round(player.medicUbers / player.medicGames, 2)
    player.medicUD = round(player.medicUD / player.medicGames, 2)
    player.medicHPM = round(player.medicHeals / player.medicGames, 2)
    player.medicKills = round(player.medicKills / player.medicGames, 2)
    player.medicAssists = round(player.medicAssists / player.medicGames, 2)
    player.medicDeaths = round(player.medicDeaths / player.medicGames, 2)

    if config.etf2lNicks:
        player.nick = etf2l.get_nick(player.id) or player.nick

    return player

def add_player_stats(
    id: str, playerClass: str, playerClassTime: int, playerTeam: str, scoreBlu: int, scoreRed: int,
    playerDPM: int, playerKPD: float, playerKAPD: float, playerDMG: int, playerDT: int, playerDTM: float, 
    playerDAPD: float, playerHR: int, playerAirshots: int, playerKills: int, playerAssists: int, playerDeaths: int,
    playerHeal: int, playerUbers: int, playerUD: int, playerCPC: int, playerKPM: int
) -> None | Exception:
    for player in playerList:
        if player.id == id:
            player = set_stats(
                player, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
                playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDTM, playerDAPD,
                playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
                playerHeal, playerUbers, playerUD, playerCPC, playerKPM
            )
            
            return
    return exceptions.IdNotFoundException

def get_player_nick(id: str) -> str | Exception:
    for player in playerList:
        if player.id == id:
            return player.nick
    
    return exceptions.IdNotFoundException

def set_player_elo(id: str, elo: float):
    for player in playerList:
        if player.id == id:
            try:
                # if a player has a long time on a class without many kills (eg 3 kills in 15 minutes)
                # the bonus elo tanks and is a good indication of a player not really playing the game
                if player.bonusElo > -40:
                    player.eloOld = player.eloNew
                    player.eloNew = elo + player.bonusElo
                    return
            except:
                print(f"elo couldnt be set for '{get_player_nick(id)}', probably due to being subbed out")
                return

def set_player_bonus_elo(id: str, elo: int):
     for player in playerList:
        if player.id == id:
            player.bonusElo = elo
            return

def get_average_elo(player_list_in_a_game: list[float]) -> float:
    return float(sum(player_list_in_a_game) / len(player_list_in_a_game))

def is_shit_log(teams):
    for team in teams.values():
        if team['kills'] < 32:
            return True
    return False

def is_player_added(id):
    return False if next((player for player in playerList if player.id == id), None) == None else True

def get_player_elo(id: str) -> int or Exception:
    for player in playerList:
        if player.id == id:
            return player.eloNew

    return exceptions.IdNotFoundException