import stats, operator, config, xlsx, player

def show_results(playerList: list, predictionFalse: int, predictionRight: int):
    canSkipShitters: bool = config.can_skip_shitters(input("\nSkip people with less then or equal to 5 games in the final log? [y / n]; def y => ") or 'y')
    printMethod: str = config.check_export_method(input('Choose export method [print / xlsx] def print => ') or 'print')
    config.etf2lNick = config.set_etf2l_nicks(input('Change nicks to ETF2L ones? [y / n] def y => ') or 'y')
    prediction: float = round((predictionRight/(predictionFalse + predictionRight)) * 100, 3)
    print('~~~~~~~~~~~~~~~~~~~~~~~')

    playerList.sort(key = operator.attrgetter('eloNew'), reverse = True)

    if printMethod == 'print':
        for player in playerList:
            if canSkipShitters and player.gamesCount <= 5:
                continue

            # etf2lNicks are then used in this method
            player = stats.calculate_averages(player)

            print(f"{player.nick} - {round(player.eloNew)}, {round(player.eloNew - player.eloOld)}, WR - [{round((player.wins / (player.wins + player.loses) * 100), 2)}%]") 
                    # | scout: {i.scoutDPM}, {i.scoutKD} [{i.scoutGames}] | soldier: {i.soldierDPM}, {i.soldierKD} [{i.soldierGames}] | demo: {i.demoDPM}, {i.demoKD} [{i.demoGames}] | medic: {i.medicHPM}, {i.medicUbers} [{i.medicGames}]")

    elif printMethod == 'xlsx':
        xlsx.create_file(playerList, canSkipShitters)

    print(f"\n{prediction}% of matches were predicted correctly based on elo")