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
        winChance = 1/(1+10**((bluElo - playerElo)/400))
        return count_new_elo(playerElo, winChance, RF)

    elif team == 'Blue':
        winChance = 1/(1+10**((redElo - playerElo)/400))
        return count_new_elo(playerElo, winChance, BF)

    return exception.EloCouldntBeCalculated

def count_new_elo(playerElo, winChance, factor):
    return playerElo + 32(factor - winChance)
