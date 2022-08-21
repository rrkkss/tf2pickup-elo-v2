def set_stats(
    player, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
    playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
    playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
    playerHeal, playerUbers, playerUD, playerCPC, playerKPM
):
    player.gamesCount += 1

    winningTeam = get_winning_team(scoreRed, scoreBlu)
    if winningTeam != 'draw':
        if compare_string(winningTeam, playerTeam): #if the player won
            player.wins += 1
            if playerTeam == 'Blue':
                player.bluGames += 1
                player.bluWins += 1
            elif playerTeam == 'Red':
                player.redGames += 1
                player.redWins += 1
        else: #if the player lost
            player.loses += 1
            if playerTeam == 'Blue':
                player.bluGames += 1
                player.bluLoses += 1
            elif playerTeam == 'Red':
                player.redGames += 1
                player.redLoses += 1
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
        player.scoutKPM += playerKPM
        player.scoutKD += float(playerKPD)
        player.scoutKDA += float(playerKAPD)
        player.scoutKills += playerKills
        player.scoutAssists += playerAssists
        player.scoutDeaths += playerDeaths

    elif playerClass == 'soldier':
        player.soldierGames += 1
        player.soldierPlayTime += playerClassTime
        player.soldierDPM += playerDPM
        player.soldierKPM += playerKPM
        player.soldierKD += float(playerKPD)
        player.soldierKDA += float(playerKAPD)
        player.soldierAirshots += playerAirshots
        player.soldierKills += playerKills
        player.soldierAssists += playerAssists
        player.soldierDeaths += playerDeaths

    elif playerClass == 'demoman':
        player.demoGames += 1
        player.demoPlayTime += playerClassTime
        player.demoDPM += playerDPM
        player.demoKPM += playerKPM
        player.demoKD += float(playerKPD)
        player.demoKDA += float(playerKAPD)
        player.demoAirshots += playerAirshots
        player.demoKills += playerKills
        player.demoAssists += playerAssists
        player.demoDeaths += playerDeaths

    elif playerClass == 'medic':
        player.medicGames += 1
        player.medicPlayTime += playerClassTime
        player.medicDPM += playerDPM
        player.medicKPM += playerKPM
        player.medicKD += float(playerKPD)
        player.medicKDA += float(playerKAPD)
        player.medicHeals += playerHeal
        player.medicUbers += playerUbers
        player.medicKills += playerKills
        player.medicAssists += playerAssists
        player.medicDeaths += playerDeaths

    return player

def calculate_averages(player):
    if player.scoutGames == 0: player.scoutGames = 1
    if player.soldierGames == 0: player.soldierGames = 1
    if player.demoGames == 0: player.demoGames = 1
    if player.medicGames == 0: player.medicGames = 1

    player.scoutPlayTime = round(player.scoutPlayTime / 3600, 2) #in hours
    player.scoutDPM = round(player.scoutDPM / player.scoutGames, 2)
    player.scoutKPM = round(player.scoutKPM / player.scoutGames, 2)
    player.scoutKD = round(player.scoutKD / player.scoutGames, 2)
    player.scoutKDA = round(player.scoutKDA / player.scoutGames, 2)
    player.scoutKills = round(player.scoutKills / player.scoutGames, 2)
    player.scoutAssists = round(player.scoutAssists / player.scoutGames, 2)
    player.scoutDeaths = round(player.scoutDeaths / player.scoutGames, 2)

    player.soldierPlayTime = round(player.soldierPlayTime / 3600, 2)
    player.soldierDPM = round(player.soldierDPM / player.soldierGames, 2)
    player.soldierKPM = round(player.soldierKPM / player.soldierGames, 2)
    player.soldierKD = round(player.soldierKD / player.soldierGames, 2)
    player.soldierKDA = round(player.soldierKDA / player.soldierGames, 2)
    player.soldierAirshots = round(player.soldierAirshots / player.soldierGames, 2)
    player.soldierKills = round(player.soldierKills / player.soldierGames, 2)
    player.soldierAssists = round(player.soldierAssists / player.soldierGames, 2)
    player.soldierDeaths = round(player.soldierDeaths / player.soldierGames, 2)

    player.demoPlayTime = round(player.demoPlayTime / 3600, 2)
    player.demoDPM = round(player.demoDPM / player.demoGames, 2)
    player.demoKPM = round(player.demoKPM / player.demoGames, 2)
    player.demoKD = round(player.demoKD / player.demoGames, 2)
    player.demoKDA = round(player.demoKDA / player.demoGames, 2)
    player.demoAirshots = round(player.demoAirshots / player.demoGames, 2)
    player.demoKills = round(player.demoKills / player.demoGames, 2)
    player.demoAssists = round(player.demoAssists / player.demoGames, 2)
    player.demoDeaths = round(player.demoDeaths / player.demoGames, 2)

    player.medicPlayTime = round(player.medicPlayTime / 3600, 2)
    player.medicDPM = round(player.medicDPM / player.medicGames, 2)
    player.medicKPM = round(player.medicKPM / player.medicGames, 2)
    player.medicKD = round(player.medicKD / player.medicGames, 2)
    player.medicKDA = round(player.medicKDA / player.medicGames, 2)
    player.medicUbers = round(player.medicUbers / player.medicGames, 2)
    player.medicHPM = round(player.medicHeals / player.medicGames, 2)
    player.medicKills = round(player.medicKills / player.medicGames, 2)
    player.medicAssists = round(player.medicAssists / player.medicGames, 2)
    player.medicDeaths = round(player.medicDeaths / player.medicGames, 2)

    return player

def get_winning_team(red, blu):
    if blu > red:
        return 'Blue'
    elif blu < red:
        return 'Red'
    else:
        return 'draw'

def compare_string(str1, str2):
    if str1 == str2:
        return True
    return False