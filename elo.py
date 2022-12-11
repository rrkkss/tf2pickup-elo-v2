import exceptions

eloFactor = 32

def count_elo(playerElo: float, team: str, redElo: float, redScore: int, bluElo: float, bluScore: int) -> float or Exception:    
    if redScore > bluScore:
        RF = 1
        BF = 0

    elif redScore == bluScore:
        RF = 0.5
        BF = 0.5

    elif redScore < bluScore:
        RF = 0
        BF = 1

    if team == 'Red':
        return count_new_elo(playerElo, count_win_chance(bluElo, playerElo), RF)

    elif team == 'Blu':
        return count_new_elo(playerElo, count_win_chance(redElo, playerElo), BF)

    return exceptions.EloCouldntBeCalculated

def count_new_elo(playerElo: float, winChance: float, factor: float) -> float:
    return playerElo + eloFactor*(factor - winChance)

def count_win_chance(enemyElo: float, yourElo: float) -> float:
    return (1/(1+10**((enemyElo - yourElo)/400)))

def calculate_bonus_elo(playerClass: str, playerKPD: float, playerKAPD: float, playerDPM: int, playerDMG: int, playerDT: int, playerHeal: int, playerCPC: int, gameLength: int) -> float or Exception:
    if playerClass == 'scout':
        return (float(playerKAPD) - 2)*2 + (float(playerDPM) - 250)/20 + float(playerCPC)/5
            
    elif playerClass == 'soldier':
        return (float(playerKPD) - 0.7)*3 + (float(playerDPM) - 285)/15 + (float(playerDMG) - float(playerDT))/400

    elif playerClass == 'demoman':
        return (float(playerKPD) - 1.3)*5 + (float(playerDPM) - 340)/20 + (float(playerKAPD) - 1.5)*5

    elif  playerClass == 'medic':
        return (float(playerKAPD) - 1.5)*5 + (float(playerHeal))**(1/8) + (float(playerHeal / (gameLength / 60.0)) - 850)/100

    return exceptions.EloCouldntBeCalculated