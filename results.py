import stats, operator, config, xlsx

def show_results(player_list: list, prediction_false: int, prediction_right: int):
    can_skip_shitters: bool = config.can_skip_shitters(input("\nSkip people with less then or equal to 5 games in the final log? [y / n]; def y => ") or 'y')
    print_method: str = config.check_export_method(input('Choose export method [print / xlsx] def xlsx => ') or 'xlsx')
    config.etf2lNick = config.set_etf2l_nicks(input('Change nicks to ETF2L ones? [y / n] def y => ') or 'y')
    prediction: float = round((prediction_right/(prediction_false + prediction_right)) * 100, 3)
    print('~~~~~~~~~~~~~~~~~~~~~~~')

    player_list.sort(key = operator.attrgetter('eloNew'), reverse = True)

    if print_method == 'print':
        for player in player_list:
            if can_skip_shitters and player.gamesCount <= 5:
                continue

            player = stats.calculate_averages(player)

            print(f"{player.nick} - {round(player.eloNew)}, {round(player.eloNew - player.eloOld)}, WR - [{round((player.wins / (player.wins + player.loses) * 100), 2)}%]") 

    elif print_method == 'xlsx':
        xlsx.create_file(player_list, can_skip_shitters)

    print(f"\n{prediction}% of matches were predicted correctly based on elo")