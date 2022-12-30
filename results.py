import stats
import operator

def show_results(playerList: list, predictionFalse: int, predictionRight: int, canSkipShitters: bool):
    print('~~~~~~~~~~~~~~~~~~~~~~~')
    
    playerList.sort(key = operator.attrgetter('eloNew'), reverse = True)

    for i in playerList:
        if canSkipShitters and i.gamesCount <= 5:
            continue

        i = stats.calculate_averages(i)

        print(f"{i.nick} - {round(i.eloNew)}, {round(i.eloNew - i.eloOld)} [{round((i.wins/(i.wins+i.loses)*100),2)}%]") # | scout: {i.scoutDPM}, {i.scoutKD} [{i.scoutGames}] | soldier: {i.soldierDPM}, {i.soldierKD} [{i.soldierGames}] | demo: {i.demoDPM}, {i.demoKD} [{i.demoGames}] | medic: {i.medicHPM}, {i.medicUbers} [{i.medicGames}]")
    
    print(f"\n{round((predictionRight/(predictionFalse + predictionRight)) * 100, 3)}% of matches were predicted correctly based on elo")