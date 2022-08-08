import requests
import time
import player
import exception
import elo
import eloBonus
import predictions
import operator

playerList = []
predictionRight = 0
predictionFalse = 0
canAddBonusElo = True
countEloIndividually = False
canSkipShitters = True

def get_logs():
    search = input("\nEnter log title keyword, def 'tf2pickup.cz' => ") or 'tf2pickup.cz'
    wait = input("Enter wait time inbetween logs, def 0.4 => ") or 0.4
    wait = is_wait_number_valid(wait)
    can_add_bonus_elo(input("Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y => ") or 'y')
    count_elo_individually(input("Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n => ") or 'n')
    can_skip_shitters(input("Skip people with less then 5 games in the final log? [y / n]; def y => ") or 'y')

    url = 'http://logs.tf/api/v1/log?title=' + search + '&limit=5000'
    print(f"\nparsing from: {url}")

    try:
        j = requests.get(url).json()
    except Exception as e:
        print(f"{e} \n json couldn't be parsed")
        quit()

    results = list(j.values())[1]

    if search == 'tf2pickup.cz':
        results = results - 24 # comment below, it was 24 of them

    if results > 0:
        print(f"Found {results} results\n")
        parse_logs(create_log_list(j, search), wait, results)
    else:
        print(f"Found {results} results, try another search term")
        get_logs()

def create_log_list(json, title):
    logList = []

    for i in json:
        if i == 'logs':
            for k in json[i]:
                n = list(k.values())
                if title == 'tf2pickup.cz':
                    if int(n[0]) < 2865412: # first actual czech pug, before that 24 dmixes were under the same title
                        break
                logList.append(n[0])

    return logList

def parse_logs(logList, wait, results):
    count = 0 
    # for i in logList: # for testing purposes
    for i in reversed(logList):
        count += 1
        # if count > 10:
        #     break
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(i)

        try:
            j = requests.get(url).json()
            if j['success'] == True:
                print(f"OK - {url} [{count}/{results}]")
            if is_shit_log(j['teams']):
                print(f"~~~ Shit log detected, skipping")
                continue
        except:
            print(f"FAILED - {url} [{count}/{results}]: nothing to parse, skipping. Wait time probably too SHORT")
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
            playerList.append(player.createPlayer(k, v))
    
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
                eloBonus.calculate_bonus_elo(
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
    for i in teams.items():
        if i[1]['kills'] < 32:
            return True
    return False

def get_scores_from_data(j, team):
    for x in j["teams"].items():
        if x[0] == team:
            return x[1]["score"]

def is_player_added(id):
    for i in playerList:
        if i.id == id:
            return True
    return False

def get_player_elo(id):
    for i in playerList:
        if i.id == id:
            return i.eloNew
    return exception.IdNotFoundException

def loop_over_team(id, playerTeam, teamRedElo, scoreRed, teamBluElo, scoreBlu):
    if countEloIndividually:
        eloInFocus = get_player_elo(id)
    elif playerTeam == 'Red':
        eloInFocus =get_average_elo(teamRedElo)
    elif playerTeam == 'Blu':
        eloInFocus =get_average_elo(teamBluElo)

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

def get_average_elo(list):
    count = 0
    for i in list:
        count += float(i)

    return float(count/len(list))

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

def is_wait_number_valid(num):
    isNumberValid = False

    while isNumberValid == False:  
        try:
            num = float(num)
            if num >= 0:
                isNumberValid = True
            else:
                num = list(num) # definitely ugly design, but it works hey
        except:
            num = input(f"Not a valid number, enter a new one => ")

    return num

def add_player_stats(
    id, playerClass, playerClassTime, playerTeam, scoreBlu, scoreRed,
    playerDPM, playerKPD, playerKAPD, playerDMG, playerDT, playerDAPD,
    playerHR, playerAirshots, playerKills, playerAssists, playerDeaths,
    playerHeal, playerUbers, playerUD, playerCPC, playerKPM
):
    for i in playerList:
        if i.id == id:
            i.gamesCount += 1

            winningTeam = get_winning_team(scoreRed, scoreBlu)
            if winningTeam != 'draw':
                if compare_string(winningTeam, playerTeam): #if the player won
                    i.wins += 1
                    if playerTeam == 'Blue':
                        i.bluGames += 1
                        i.bluWins += 1
                    elif playerTeam == 'Red':
                        i.redGames += 1
                        i.redWins += 1
                else: #if the player lost
                    i.loses += 1
                    if playerTeam == 'Blue':
                        i.bluGames += 1
                        i.bluLoses += 1
                    elif playerTeam == 'Red':
                        i.redGames += 1
                        i.redLoses += 1
            else:
                i.draws += 1
                if playerTeam == 'Blue':
                    i.bluGames += 1
                    i.bluDraws += 1
                elif playerTeam == 'Red':
                    i.redGames += 1
                    i.redDraws += 1

            if playerClass == 'scout':
                i.scoutGames += 1
                i.scoutPlayTime += playerClassTime
                i.scoutDPM += playerDPM
                i.scoutKPM += playerKPM
                i.scoutKD += float(playerKPD)
                i.scoutKDA += float(playerKAPD)
                i.scoutKills += playerKills
                i.scoutAssists += playerAssists
                i.scoutDeaths += playerDeaths

            elif playerClass == 'soldier':
                i.soldierGames += 1
                i.soldierPlayTime += playerClassTime
                i.soldierDPM += playerDPM
                i.soldierKPM += playerKPM
                i.soldierKD += float(playerKPD)
                i.soldierKDA += float(playerKAPD)
                i.soldierAirshots += playerAirshots
                i.soldierKills += playerKills
                i.soldierAssists += playerAssists
                i.soldierDeaths += playerDeaths

            elif playerClass == 'demoman':
                i.demoGames += 1
                i.demoPlayTime += playerClassTime
                i.demoDPM += playerDPM
                i.demoKPM += playerKPM
                i.demoKD += float(playerKPD)
                i.demoKDA += float(playerKAPD)
                i.demoAirshots += playerAirshots
                i.demoKills += playerKills
                i.demoAssists += playerAssists
                i.demoDeaths += playerDeaths

            elif playerClass == 'medic':
                i.medicGames += 1
                i.medicPlayTime += playerClassTime
                i.medicDPM += playerDPM
                i.medicKPM += playerKPM
                i.medicKD += float(playerKPD)
                i.medicKDA += float(playerKAPD)
                i.medicHeals += playerHeal
                i.medicUbers += playerUbers
                i.medicKills += playerKills
                i.medicAssists += playerAssists
                i.medicDeaths += playerDeaths

def get_winning_team(red, blu):
    if blu > red:
        return 'Blue'
    elif blu < red:
        return 'Red'
    else:
        return 'draw'

def compare_string(str1, str2):
    if str1 == str2:
        return True
    return False

def calculate_averages():
    for i in playerList:
        if i.scoutGames == 0: i.scoutGames = 1
        if i.soldierGames == 0: i.soldierGames = 1
        if i.demoGames == 0: i.demoGames = 1
        if i.medicGames == 0: i.medicGames = 1

        i.scoutPlayTime = round(i.scoutPlayTime / 3600, 2) #in hours
        i.scoutDPM = round(i.scoutDPM / i.scoutGames, 2)
        i.scoutKPM = round(i.scoutKPM / i.scoutGames, 2)
        i.scoutKD = round(i.scoutKD / i.scoutGames, 2)
        i.scoutKDA = round(i.scoutKDA / i.scoutGames, 2)
        i.scoutKills = round(i.scoutKills / i.scoutGames, 2)
        i.scoutAssists = round(i.scoutAssists / i.scoutGames, 2)
        i.scoutDeaths = round(i.scoutDeaths / i.scoutGames, 2)

        i.soldierPlayTime = round(i.soldierPlayTime / 3600, 2)
        i.soldierDPM = round(i.soldierDPM / i.soldierGames, 2)
        i.soldierKPM = round(i.soldierKPM / i.soldierGames, 2)
        i.soldierKD = round(i.soldierKD / i.soldierGames, 2)
        i.soldierKDA = round(i.soldierKDA / i.soldierGames, 2)
        i.soldierAirshots = round(i.soldierAirshots / i.soldierGames, 2)
        i.soldierKills = round(i.soldierKills / i.soldierGames, 2)
        i.soldierAssists = round(i.soldierAssists / i.soldierGames, 2)
        i.soldierDeaths = round(i.soldierDeaths / i.soldierGames, 2)

        i.demoPlayTime = round(i.demoPlayTime / 3600, 2)
        i.demoDPM = round(i.demoDPM / i.demoGames, 2)
        i.demoKPM = round(i.demoKPM / i.demoGames, 2)
        i.demoKD = round(i.demoKD / i.demoGames, 2)
        i.demoKDA = round(i.demoKDA / i.demoGames, 2)
        i.demoAirshots = round(i.demoAirshots / i.demoGames, 2)
        i.demoKills = round(i.demoKills / i.demoGames, 2)
        i.demoAssists = round(i.demoAssists / i.demoGames, 2)
        i.demoDeaths = round(i.demoDeaths / i.demoGames, 2)

        i.medicPlayTime = round(i.medicPlayTime / 3600, 2)
        i.medicDPM = round(i.medicDPM / i.medicGames, 2)
        i.medicKPM = round(i.medicKPM / i.medicGames, 2)
        i.medicKD = round(i.medicKD / i.medicGames, 2)
        i.medicKDA = round(i.medicKDA / i.medicGames, 2)
        i.medicUbers = round(i.medicUbers / i.medicGames, 2)
        i.medicHPM = round(i.medicHeals / i.medicGames, 2)
        i.medicKills = round(i.medicKills / i.medicGames, 2)
        i.medicAssists = round(i.medicAssists / i.medicGames, 2)
        i.medicDeaths = round(i.medicDeaths / i.medicGames, 2)

def show_result():
    print('~~~~~~~~~~~~~~~~~~~~~~~')
    
    playerList.sort(key = operator.attrgetter('eloNew'), reverse = True)

    calculate_averages()

    for i in playerList:
        if canSkipShitters:
            if i.gamesCount <= 5:
                continue

        print(f"{i.nick} - {round(i.eloNew)}, {round(i.eloNew - i.eloOld)} [{round((i.wins/(i.wins+i.loses)*100),2)}%] | scout: {i.scoutDPM}, {i.scoutKD} [{i.scoutGames}] | soldier: {i.soldierDPM}, {i.soldierKD} [{i.soldierGames}] | demo: {i.demoDPM}, {i.demoKD} [{i.demoGames}] | medic: {i.medicHPM}, {i.medicUbers} [{i.medicGames}]")
    
    print(f"\n{round((predictionRight/(predictionFalse + predictionRight)) * 100, 3)}% of matches were predicted correctly based on elo")