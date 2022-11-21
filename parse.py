import requests
import time
import player
import exceptions
import elo
import predictions
import stats

playerList = []
predictionRight = 0
predictionFalse = 0
canAddBonusElo = True
countEloIndividually = False
canSkipShitters = True

def init_parse():
    search = input("\nEnter log title keyword, def 'tf2pickup.cz' => ") or 'tf2pickup.cz'
    wait = input("Enter wait time inbetween logs, def 0.4 => ") or 0.4
    wait = is_wait_number_valid(wait)
    can_add_bonus_elo(input("Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y => ") or 'y')
    count_elo_individually(input("Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n => ") or 'n')
    can_skip_shitters(input("Skip people with less then 5 games in the final log? [y / n]; def y => ") or 'y')
    set_elo_factor(input("Set elo factor [number]; def 32 => ") or 32)

    get_logs(search, wait)

def change_search_term(wait):
    search = input("\nEnter different keyword' => ")
    get_logs(search, wait)

def get_logs(search, wait):
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
        print(f"Found {results} results, try another search term")
        change_search_term(wait)

def create_log_list(json):
    logList = []

    for log in json['logs']:
        logList.append(log['id'])

    return logList

def parse_logs(logList, wait, results):
    for index, i in enumerate(reversed(logList)):
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(i)

        try:
            json = requests.get(url).json()
            if json['success'] == True:
                print(f"OK - {url} [{index+1}/{results}]")
            if is_shit_log(json['teams']):
                print(f"~~~ Shit log detected, skipping")
                continue
        except:
            print(f"FAILED - {url} [{index+1}/{results}]: nothing to parse, skipping. Wait time probably too SHORT")
            continue

        get_data_from_log(json)

def get_data_from_log(json):
    nicks = json['names']
    teamRed = []
    teamRedElo = []
    teamBlu = []
    teamBluElo = []

    for k, v in nicks.items():
        if is_player_added(k) == False:
            playerList.append(player.createPlayer(k, v))
    
    gameLength = int(json['length']) # in seconds
    scoreRed = get_scores_from_json(json, 'Red')
    scoreBlu = get_scores_from_json(json, 'Blue')

    for p in json['players'].items():
        playerID = p[0]
        playerInfo = dict(p[1].items())
        playerClass = playerInfo['class_stats'][0]['type']
        playerClassTime = playerInfo['class_stats'][0]['total_time']
        playerTeam = playerInfo['team']
        playerDPM = playerInfo['dapm']          # damage per minute
        playerKPD = playerInfo['kpd']           # kill per death
        playerKAPD = playerInfo['kapd']         # kill + assist per death
        playerDMG = playerInfo['dmg']
        playerDT = playerInfo['dt']             # damage taken
        playerDAPD = playerInfo['dapd']         # damage per death
        playerHR = playerInfo['hr']             # heals recieved
        playerAirshots = playerInfo['as']
        playerKills = playerInfo['kills']
        playerAssists = playerInfo['assists']
        playerDeaths = playerInfo['deaths']
        playerHeal = playerInfo['heal']
        playerUbers = playerInfo['ubers']
        playerUD = playerInfo['drops']
        playerCPC = playerInfo['cpc']
        playerKPM = playerKills / (gameLength / 60) # kills per minute

        if playerTeam == 'Red':
            teamRed.append(playerID)
            teamRedElo.append(get_player_elo(playerID))
        elif playerTeam == 'Blue':
            teamBlu.append(playerID)
            teamBluElo.append(get_player_elo(playerID))

        if canAddBonusElo:
            set_player_bonus_elo(
                playerID,
                elo.calculate_bonus_elo(
                    playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength
                )
            )
        
        add_player_stats(
            playerID, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
            playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
            playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
            playerHeal, playerUbers, playerUD, playerCPC, playerKPM
        )

    #print(f"BLU [{scoreBlu}]: {round(get_average_elo(teamBluElo))} ({round(elo.count_win_chance(get_average_elo(teamRedElo), get_average_elo(teamBluElo)), 2)}%), RED [{scoreRed}]: {round(get_average_elo(teamRedElo))} ({round(elo.count_win_chance(get_average_elo(teamBluElo), get_average_elo(teamRedElo)), 2)}%) \n")
    
    if (predictions.was_prediction_right(
            scoreBlu, scoreRed, 
            elo.count_win_chance(get_average_elo(teamRedElo), get_average_elo(teamBluElo)),
            elo.count_win_chance(get_average_elo(teamBluElo), get_average_elo(teamRedElo)))):
        global predictionRight
        predictionRight += 1
    else:
        global predictionFalse
        predictionFalse += 1

    for i in teamRed:
        loop_over_team(i, 'Red', teamRedElo, scoreRed, teamBluElo, scoreBlu)

    for i in teamBlu:
        loop_over_team(i, 'Blu', teamRedElo, scoreRed, teamBluElo, scoreBlu)
        
def is_shit_log(teams):
    for team in teams.values():
        if team['kills'] < 32:
            return True
    return False

def get_scores_from_json(json, team):
    for x in json['teams'].items():
        if x[0] == team:
            return x[1]['score']

def is_player_added(id):
    return False if next((player for player in playerList if player.id == id), None) == None else True

def get_player_elo(id):
    for i in playerList:
        if i.id == id:
            return i.eloNew
    return exceptions.IdNotFoundException

def loop_over_team(id, playerTeam, teamRedElo, scoreRed, teamBluElo, scoreBlu):
    if countEloIndividually:
        eloInFocus = get_player_elo(id)
    elif playerTeam == 'Red':
        eloInFocus = get_average_elo(teamRedElo)
    elif playerTeam == 'Blu':
        eloInFocus = get_average_elo(teamBluElo)

    set_player_elo(
        id, elo.count_elo(
            eloInFocus, playerTeam,
            get_average_elo(teamRedElo), scoreRed,
            get_average_elo(teamBluElo), scoreBlu
        )
    )

def get_player_nick(id):
    for i in playerList:
        if i.id == id:
            return i.nick

def set_player_elo(id, elo):
    for i in playerList:
        if i.id == id:
            try:
                if i.bonusElo > -40:
                    i.eloOld = i.eloNew
                    i.eloNew = elo + i.bonusElo
            except:
                print(f"elo couldnt be set for '{get_player_nick(id)}', probably due to being subbed out")

def set_player_bonus_elo(id, elo):
     for i in playerList:
        if i.id == id:
            i.bonusElo = elo

def get_average_elo(playerList):
    return float(sum(playerList) / len(playerList))

def can_add_bonus_elo(input): # def true
    global canAddBonusElo

    if input == 'n' or input == 'n':
        canAddBonusElo = False

def count_elo_individually(input): # def false
    global countEloIndividually

    if input == 'y' or input == 'Y':
        countEloIndividually = True

def can_skip_shitters(input): # def true
    global canSkipShitters

    if input == 'n' or input == 'N':
        canSkipShitters = False

def set_elo_factor(num):
    isValid = False

    while isValid == False:
        try:
            num = int(num)
            if num > 0:
                isValid = True
            else:
                num = list(num)
        except:
            num = input(f"Not a valid number, please enter a new one => ")

    elo.eloFactor = num

def is_wait_number_valid(num):
    isNumberValid = False

    if not is_number_valid(num):
        while isNumberValid == False:
            num = input(f"Not a valid number, enter a new one => ")
            if is_number_valid(num):
                isNumberValid = True
    
    return float(num)

def is_number_valid(num):
    try:
        float(num)
        return True
    except:
        return False

def add_player_stats(
    id, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
    playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
    playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
    playerHeal, playerUbers, playerUD, playerCPC, playerKPM
):
    for i in playerList:
        if i.id == id:
            i = stats.set_stats(
                i, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
                playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
                playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
                playerHeal, playerUbers, playerUD, playerCPC, playerKPM
            )

def compare_string(str1, str2):
    if str1 == str2:
        return True
    return False

def calculate_averages():
    for i in playerList:
        i = stats.calculate_averages(i)