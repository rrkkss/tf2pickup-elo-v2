import requests, time, player, elo, predictions, stats, general, setup

def init_parse():
    search = input("\nEnter log title keyword, def 'tf2pickup.cz' => ") or 'tf2pickup.cz'
    wait = input("Enter wait time inbetween logs, def 0.4 => ") or 0.4
    wait = general.is_wait_number_valid(wait)
    setup.can_add_bonus_elo(input("Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y => ") or 'y')
    setup.count_elo_individually(input("Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n => ") or 'n')
    setup.can_skip_shitters(input("Skip people with less then 5 games in the final log? [y / n]; def y => ") or 'y')
    elo.eloFactor = general.set_elo_factor(input("Set elo factor [number]; def 32 => ") or 32)

    get_logs(search, wait)

def change_search_term(wait: float):
    search = input("\nEnter different keyword' => ")
    get_logs(search, wait)

def get_logs(search: str, wait: float):
    url = 'http://logs.tf/api/v1/log?title=' + search + '&limit=5000'
    print(f"\nparsing from: {url}")

    try:
        json = requests.get(url).json()
    except Exception as e:
        print(f"{e} \n json couldn't be parsed")
        quit()

    logList = create_log_list(json)

    if len(logList) > 0:
        print(f"Found {logList.__len__()} results\n")
        parse_logs(logList, wait, len(logList))
    else:
        print(f"Found {logList.__len__()} results, try another search term")
        change_search_term(wait)

def create_log_list(json) -> list:
    logList = []

    for log in json['logs']:
        logList.append(log['id'])

    return logList

def parse_logs(logList: list, wait: float, results: int):
    for index, i in enumerate(reversed(logList)):
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(i)

        try:
            json = requests.get(url).json()
            if json['success'] == True:
                print(f"OK - {url} [{index+1}/{results}]")
            if stats.is_shit_log(json['teams']):
                print(f"~~~ Shit log detected, skipping")
                continue
        except:
            print(f"FAILED - {url} [{index+1}/{results}]: nothing to parse, skipping. Wait time probably too SHORT")
            continue

        get_data_from_log(json)

def get_data_from_log(json):
    nicks = json['names']
    teamRed = []; teamRedElo = []; teamBlu = []; teamBluElo = []

    for k, v in nicks.items():
        if stats.is_player_added(k) == False:
            stats.playerList.append(player.createPlayer(k, v))
    
    gameLength = int(json['length']) # in seconds
    scoreRed = get_scores_from_json(json, 'Red')
    scoreBlu = get_scores_from_json(json, 'Blue')

    for p in json['players'].items():
        playerID = p[0]
        playerInfo = dict(p[1].items())
        playerClassStats = playerInfo['class_stats'][0]
        playerClass = playerClassStats['type']
        playerClassTime = int(playerClassStats['total_time']) #cba honestly
        playerTeam = playerInfo['team']
        playerDPM = int(playerInfo['dapm'])             # damage per minute
        playerKPD = float(playerInfo['kpd'])            # kill per death
        playerKAPD = float(playerInfo['kapd'])          # kill + assist per death
        playerDMG = int(playerInfo['dmg'])
        playerDT = int(playerInfo['dt'])                # damage taken
        playerDAPD = float(playerInfo['dapd'])          # damage per death
        playerHR = int(playerInfo['hr'])                # heals recieved
        playerAirshots = int(playerInfo['as'])
        playerKills = int(playerInfo['kills'])
        playerAssists = int(playerInfo['assists'])
        playerDeaths = int(playerInfo['deaths'])
        playerHeal = int(playerInfo['heal'])
        playerUbers = int(playerInfo['ubers'])
        playerUD = int(playerInfo['drops'])
        playerCPC = int(playerInfo['cpc'])
        playerKPM = playerKills / (gameLength / 60)     # kills per minute

        if playerTeam == 'Red':
            teamRed.append(playerID)
            teamRedElo.append(stats.get_player_elo(playerID))
        elif playerTeam == 'Blue':
            teamBlu.append(playerID)
            teamBluElo.append(stats.get_player_elo(playerID))

        if setup.canAddBonusElo:
            stats.set_player_bonus_elo(
                playerID, elo.calculate_bonus_elo(
                    playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength
                )
            )
        
        stats.add_player_stats(
            playerID, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
            playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
            playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
            playerHeal, playerUbers, playerUD, playerCPC, playerKPM
        )

    if (predictions.was_prediction_right(
            scoreBlu, scoreRed, 
            elo.count_win_chance(stats.get_average_elo(teamRedElo), stats.get_average_elo(teamBluElo)),
            elo.count_win_chance(stats.get_average_elo(teamBluElo), stats.get_average_elo(teamRedElo))
    )):
        stats.predictionRight += 1
    else:
        stats.predictionFalse += 1

    for i in teamRed:
        loop_over_team(i, 'Red', teamRedElo, scoreRed, teamBluElo, scoreBlu)

    for i in teamBlu:
        loop_over_team(i, 'Blu', teamRedElo, scoreRed, teamBluElo, scoreBlu)

def get_scores_from_json(json, team: str) -> int:
    for x in json['teams'].items():
        if x[0] == team:
            return int(x[1]['score'])

def loop_over_team(id: str, playerTeam: str, teamRedElo: float, scoreRed: int, teamBluElo: float, scoreBlu: int):
    if setup.countEloIndividually:
        eloInFocus = stats.get_player_elo(id)
    elif playerTeam == 'Red':
        eloInFocus = stats.get_average_elo(teamRedElo)
    elif playerTeam == 'Blu':
        eloInFocus = stats.get_average_elo(teamBluElo)

    stats.set_player_elo(
        id, elo.count_elo(
            eloInFocus, playerTeam,
            stats.get_average_elo(teamRedElo), scoreRed,
            stats.get_average_elo(teamBluElo), scoreBlu
        )
    )
