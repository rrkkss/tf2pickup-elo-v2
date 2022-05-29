import exception

def calculate_bonus_elo(playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength):
    if playerClass == 'scout':
        return (float(playerKAPD) - 1.7)*5 + (float(playerDPM) - 240)/20 + float(playerCPC)/5
            
    elif playerClass == 'soldier':
        return (float(playerKPD) - 1)*5 + (float(playerDPM) - 280)/20 + (float(playerDMG) - float(playerDT))/500

    elif playerClass == 'demoman':
        return (float(playerKPD) - 1.5)*7 + (float(playerDPM) - 330)/20 + (float(playerKPD) - 1.5)*2

    elif  playerClass == 'medic':
        return (float(playerKAPD) - 1.5)*5 + (float(playerHeal))**(1/5) + (float(playerHeal / (gameLength / 60.0)) - 800)/25

    return exception.EloCouldntBeCalculated