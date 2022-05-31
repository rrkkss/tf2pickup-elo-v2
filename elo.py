import exception

def count_elo(playerElo, team, redElo, redScore, bluElo, bluScore):    
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

    return exception.EloCouldntBeCalculated

def count_new_elo(playerElo, winChance, factor):
    return playerElo + 32*(factor - winChance)

def count_win_chance(enemyElo, yourElo):
    return (1/(1+10**((enemyElo - yourElo)/400)))