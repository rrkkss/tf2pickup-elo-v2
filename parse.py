import time, player, elo, predictions, stats, config, exceptions

try:
    # xlsxwriter is unused, but it's an early check for an optional xlsx output
    import requests, xlsxwriter
except Exception as e:
    print(f"Couldn't import module(s): {e}")
    print("Did you run 'pip install -r requirements.txt' ?")
    quit()

def init_parse():
    config.init_setup(elo)
    get_logs(config.search, config.wait)

def change_search_term(wait: float):
    search = input("\nEnter different keyword' => ")
    get_logs(search, wait)

def get_logs(search: str, wait: float):
    url = f"http://logs.tf/api/v1/log?title={search}&limit=5000"
    print(f"\nparsing from: {url}")

    try:
        json = requests.get(url).json()
    except Exception as e:
        print(f"{e} \n Json couldn't be parsed")
        quit()

    log_list = create_log_id_list(json)

    if len(log_list) > 0:
        print(f"Found {len(log_list)} results\n")
        parse_logs(log_list, wait, len(log_list))
    else:
        print("Found 0 results, try another search term")
        change_search_term(wait)

def create_log_id_list(json) -> list:
    log_list = []; last_date = ''

    for log in json['logs']:
        if last_date != log['date']:
            log_list.append(log['id'])

        last_date = log['date']

    return log_list

def parse_logs(log_list: list, wait: float, results: int):
    for index, log in enumerate(reversed(log_list)):
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(log)

        try:
            json = requests.get(url).json()
            if json['success'] == True:
                print(f"OK - {url} [{index+1}/{results}]")
            if stats.is_shit_log(json['teams']):
                print("INFO - Shit log detected, skipping")
                continue
        except:
            print(f"FAILED - {url} [{index+1}/{results}]: nothing to parse, skipping. Wait time probably too SHORT")
            continue

        get_data_from_log(json)

def get_data_from_log(json):
    nicks = json['names']

    # 11 to 15 people for sixes game
    # 11 -> one isn't in logs (maybe bad name w/e)
    # 15 -> a game with 3 subs, which I think will RARELY get above
    if len(nicks) <= config.lowestSixesPlayerCount or len(nicks) > config.highestSixesPlayerCount:
        print("INFO - Non-sixes log detected, skipping")
        return

    team_red = []; team_red_elo = []; team_blu = []; team_blu_elo = []

    for k, v in nicks.items():
        if stats.is_player_added(k) == False:
            stats.playerList.append(player.create_player(k, v))
    
    game_length = int(json['length']) # in seconds
    score_red = get_scores_from_json(json, 'Red')
    score_blu = get_scores_from_json(json, 'Blue')

    for p in json['players'].items():
        player_id = p[0]
        player_info = dict(p[1].items())
        player_class_stats = player_info['class_stats'][0]
        player_class = player_class_stats['type']
        player_class_time = int(player_class_stats['total_time'])
        player_team = player_info['team']
        playerDPM = int(player_info['dapm'])             # damage per minute
        playerKPD = float(player_info['kpd'])            # kill per death
        playerKAPD = float(player_info['kapd'])          # kill + assist per death
        playerDMG = int(player_info['dmg'])
        playerDT = int(player_info['dt'])                # damage taken
        playerDTM = float(player_info['dt']) / (game_length / 60) # damage taken per minute

        playerDAPD = float(player_info['dapd'])          # damage per death
        playerHR = int(player_info['hr'])                # heals recieved
        playerAirshots = int(player_info['as'])
        playerKills = int(player_info['kills'])
        playerAssists = int(player_info['assists'])
        playerDeaths = int(player_info['deaths'])
        playerHeal = int(player_info['heal'])
        playerUbers = int(player_info['ubers'])
        playerUD = int(player_info['drops'])
        playerCPC = int(player_info['cpc'])
        playerKPM = playerKills / (game_length / 60)     # kills per minute

        if player_team == 'Red':
            team_red.append(player_id)
            team_red_elo.append(stats.get_player_elo(player_id))
        elif player_team == 'Blue':
            team_blu.append(player_id)
            team_blu_elo.append(stats.get_player_elo(player_id))

        if config.canAddBonusElo:
            stats.set_player_bonus_elo(
                player_id, elo.calculate_bonus_elo(
                    player_class, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, game_length
                )
            )
        
        stats.add_player_stats(
            player_id, player_class, player_class_time, player_team, score_blu, score_red,
            playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDTM, playerDAPD,
            playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
            playerHeal, playerUbers, playerUD, playerCPC, playerKPM
        )

    if (predictions.was_prediction_right(
            score_blu, score_red, 
            elo.count_win_chance(stats.get_average_elo(team_red_elo), stats.get_average_elo(team_blu_elo)),
            elo.count_win_chance(stats.get_average_elo(team_blu_elo), stats.get_average_elo(team_red_elo))
    )):
        stats.predictionRight += 1
    else:
        stats.predictionFalse += 1

    for p in team_red:
        loop_over_team(p, 'Red', team_red_elo, score_red, team_blu_elo, score_blu)

    for p in team_blu:
        loop_over_team(p, 'Blu', team_red_elo, score_red, team_blu_elo, score_blu)

def get_scores_from_json(json, team: str) -> int:
    for x in json['teams'].items():
        if x[0] == team:
            return int(x[1]['score'])
    
    return exceptions.ScoreCouldntBeFound

def loop_over_team(id: str, player_team: str, team_red_elo: list[float], score_red: int, team_blu_elo: list[float], score_blu: int):
    avg_blu_elo = stats.get_average_elo(team_red_elo)
    avg_red_elo = stats.get_average_elo(team_blu_elo)
    
    if config.countEloIndividually:
        elo_in_focus = stats.get_player_elo(id)
    elif player_team == 'Red':
        elo_in_focus = avg_red_elo
    elif player_team == 'Blu':
        elo_in_focus = avg_blu_elo

    stats.set_player_elo(
        id, elo.count_elo(
            elo_in_focus, player_team,
            avg_red_elo, score_red,
            avg_blu_elo, score_blu
        )
    )