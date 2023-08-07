import time, player, elo, predictions, stats, general, config

try:
    import requests, xlsxwriter
except Exception as e:
    print(f"Couldn't import module(s): {e}")
    print(f"Did you run 'pip install -r requirements.txt' ?")
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

    logList = create_log_id_list(json)

    if len(logList) > 0:
        print(f"Found {len(logList)} results\n")
        parse_logs(logList, wait, len(logList))
    else:
        print(f"Found 0 results, try another search term")
        change_search_term(wait)

def create_log_id_list(json) -> list:
    logList = []; lastDate = ''; lastTitle = ''

    for log in json['logs']:
        if lastDate != log['date']:
            logList.append(log['id'])

        lastDate = log['date']
        lastTitle = log['title']

    return logList

def parse_logs(logList: list, wait: float, results: int):
    for index, log in enumerate(reversed(logList)):
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(log)

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

    # 11 to 15 people for sixes game
    # 11 -> one isn't in logs (maybe bad name w/e)
    # 15 -> game with 3 subs, which I think will RARELY get over
    if len(nicks) < 10 or len(nicks) > 16:
        print(f"~~~ Non-sixes log detected, skipping")
        return

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
        playerClassTime = int(playerClassStats['total_time'])
        playerTeam = playerInfo['team']
        playerDPM = int(playerInfo['dapm'])             # damage per minute
        playerKPD = float(playerInfo['kpd'])            # kill per death
        playerKAPD = float(playerInfo['kapd'])          # kill + assist per death
        playerDMG = int(playerInfo['dmg'])
        playerDT = int(playerInfo['dt'])                # damage taken
        playerDTM = float(playerInfo['dt']) / (gameLength / 60) # damage taken per minute

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

        if config.canAddBonusElo:
            stats.set_player_bonus_elo(
                playerID, elo.calculate_bonus_elo(
                    playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength
                )
            )
        
        stats.add_player_stats(
            playerID, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
            playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDTM, playerDAPD,
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

    for p in teamRed:
        loop_over_team(p, 'Red', teamRedElo, scoreRed, teamBluElo, scoreBlu)

    for p in teamBlu:
        loop_over_team(p, 'Blu', teamRedElo, scoreRed, teamBluElo, scoreBlu)

def get_scores_from_json(json, team: str) -> int:
    for x in json['teams'].items():
        if x[0] == team:
            return int(x[1]['score'])
    
    return exceptions.ScoreCouldntBeFound

def loop_over_team(id: str, playerTeam: str, teamRedElo: list[float], scoreRed: int, teamBluElo: list[float], scoreBlu: int):
    avgBluElo = stats.get_average_elo(teamRedElo)
    avgRedElo = stats.get_average_elo(teamBluElo)
    
    if config.countEloIndividually:
        eloInFocus = stats.get_player_elo(id)
    elif playerTeam == 'Red':
        eloInFocus = avgRedElo
    elif playerTeam == 'Blu':
        eloInFocus = avgBluElo

    stats.set_player_elo(
        id, elo.count_elo(
            eloInFocus, playerTeam,
            avgRedElo, scoreRed,
            avgRedElo, scoreBlu
        )
    )