import stats
import operator

def can_skip_shitters(input: str):
    if input == 'y' or input == 'Y':
        return True
    else:
        return False

def show_results(playerList: list, predictionFalse: int, predictionRight: int):
    canSkipShitters: bool = can_skip_shitters(input("\nSkip people with less then or equal to 5 games in the final log? [y / n]; def y => ") or 'y')
    prediction: float = round((predictionRight/(predictionFalse + predictionRight)) * 100, 3)
    print('~~~~~~~~~~~~~~~~~~~~~~~')

    playerList.sort(key = operator.attrgetter('eloNew'), reverse = True)

    for player in playerList:
        if canSkipShitters and player.gamesCount <= 5:
            continue

        player = stats.calculate_averages(player)

        print(f"{player.nick} - {round(player.eloNew)}, {round(player.eloNew - player.eloOld)}, WR - [{round((player.wins / (player.wins + player.loses) * 100), 2)}%]") 
                # | scout: {i.scoutDPM}, {i.scoutKD} [{i.scoutGames}] | soldier: {i.soldierDPM}, {i.soldierKD} [{i.soldierGames}] | demo: {i.demoDPM}, {i.demoKD} [{i.demoGames}] | medic: {i.medicHPM}, {i.medicUbers} [{i.medicGames}]")
    
    print(f"\n{prediction}% of matches were predicted correctly based on elo")