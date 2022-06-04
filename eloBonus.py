import exception

def calculate_bonus_elo(playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength):
    if playerClass == 'scout':
        return (float(playerKAPD) - 2)*3 + (float(playerDPM) - 260)/20 + float(playerCPC)/5
            
    elif playerClass == 'soldier':
        return (float(playerKPD) - 0.7)*3 + (float(playerDPM) - 290)/15 + (float(playerDMG) - float(playerDT))/400

    elif playerClass == 'demoman':
        return (float(playerKPD) - 1.3)*7 + (float(playerDPM) - 340)/15 + (float(playerKAPD) - 1.5)*5

    elif  playerClass == 'medic':
        return (float(playerKAPD) - 1.5)*5 + (float(playerHeal))**(1/8) + (float(playerHeal / (gameLength / 60.0)) - 850)/100

    return exception.EloCouldntBeCalculated