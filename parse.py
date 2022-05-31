import requests
import time
import player
import exception
import elo
import eloBonus
import predictions

player_list = []
predictionRight = 0
predictionFalse = 0

def get_logs():
    title = input("Enter log title keyword, def 'tf2pickup.cz' => ") or 'tf2pickup.cz'
    wait = input("Enter wait time inbetween logs, def 0.4 => ") or 0.4
    wait = float(wait)

    url = 'http://logs.tf/api/v1/log?title=' + title
    print(f"parsing from: {url}")

    try:
        j = requests.get(url).json()
    except Exception as e:
        print(f"{e} \n json couldn't be parsed")
        quit()

    results = list(j.values())
    row = results[1]

    if title == 'tf2pickup.cz':
        row = results[1]-24 # comment below, it was 24 of them
    print(f"{row} results")

    log_list = []

    for i in j:
        if i == 'logs':
            for k in j[i]:
                n = list(k.values())
                if title == 'tf2pickup.cz':
                    if int(n[0]) < 2865412: # first actual czech pug, before that 24 dmixes were under the same title
                        break
                log_list.append(n[0])

    parse_logs(log_list, wait, row)

def parse_logs(log_list, wait, results):
    count = 0 # for testing purposes
    for i in log_list:
        count += 1
        # if count > 20:
        #     break
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(i)

        try:
            j = requests.get(url).json()
            if j['success'] == True:
                print(f"OK - {url} [{count}/{results}]")
            if is_shit_log(j['teams']):
                print(f"Shit log detected, skipping")
                continue
        except Exception as e:
            print(f"FAILED - {url}: {e}; bad response, failed parsing. skipping")
            continue

        get_data_from_log(j)

def get_data_from_log(j):
    nicks = dict(j['names']).items()
    teamRed = []
    teamRedElo = []
    teamBlu = []
    teamBluElo = []

    for k, v in nicks:
        if is_player_added(k) == False:
            player_list.append(player.createPlayer(k, v))
    
    gameLength = int(j['length'])
    scoreRed = get_scores_from_data(j, 'Red')
    scoreBlu = get_scores_from_data(j, 'Blue')

    for i in j['players'].items():
        playerID = i[0]
        playerInfo = dict(i[1].items())
        playerClass = playerInfo['class_stats'][0]['type']
        playerClassTime = playerInfo['class_stats'][0]['total_time']
        playerTeam = playerInfo['team']
        playerDPM = playerInfo['dapm']         # damage per minute
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
        playerKPM = int(playerKills / (gameLength / 60)) # kills per minute

        if playerTeam == 'Red':
            teamRed.append(playerID)
            teamRedElo.append(get_player_elo(playerID))
        elif playerTeam == 'Blue':
            teamBlu.append(playerID)
            teamBluElo.append(get_player_elo(playerID))

        set_player_bonus_elo(
            playerID,
            eloBonus.calculate_bonus_elo(
                playerClass, playerKPD, playerKAPD, playerDPM, playerDMG, playerDT, playerHeal, playerCPC, gameLength
            )
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
    for i in teams.items():
        if i[1]['kills'] < 32:
            return True
    return False

def get_scores_from_data(j, team):
    for x in j["teams"].items():
        if x[0] == team:
            return x[1]["score"]

def is_player_added(id):
    for i in player_list:
        if i.id == id:
            return True
    return False

def get_player_elo(id):
    for i in player_list:
        if i.id == id:
            return i.elo
    return exception.IdNotFoundException

def loop_over_team(id, playerTeam, teamRedElo, scoreRed, teamBluElo, scoreBlu):
    set_player_elo(id, 
        elo.count_elo(
            get_player_elo(id), playerTeam,
            get_average_elo(teamRedElo), scoreRed,
            get_average_elo(teamBluElo), scoreBlu
        )
    )

def get_player_name(id):
    for i in player_list:
        if i.id == id:
            return i.nick

def set_player_elo(id, elo):
    for i in player_list:
        if i.id == id:
            try:
                if i.bonusElo > -40:
                    i.elo = elo + i.bonusElo
            except:
                print(f"elo couldnt be set for '{get_player_name(id)}', probably due to being subbed out")

def set_player_bonus_elo(id, elo):
    for i in player_list:
        if i.id == id:
            i.bonusElo = elo

def get_average_elo(list):
    count = 0
    for i in list:
        count += float(i)

    return float(count/len(list))

def show_result():
    print('~~~~~~~~~~~~~~~~~~~~~~~')
    
    for i in player_list:
        print(f"{i.nick} - {round(i.elo)}")
    
    print(f"[{predictionRight}:{predictionFalse}], {(predictionRight/(predictionFalse + predictionRight)) * 100}% correct predictions")
