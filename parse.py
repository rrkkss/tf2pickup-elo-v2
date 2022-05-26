import requests
import time
import player

player_list = []

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

    parse_logs(log_list, wait)

def parse_logs(log_list, wait):
    count = 0 # for testing purposes
    for i in log_list:
        count += 1
        if count > 3:
            break
        time.sleep(wait)
        url = 'https://logs.tf/json/' + str(i)
        print('~~~~~~~~~~~~~~~~~~~~~~~')

        try:
            j = requests.get(url).json()
            if j['success'] == True:
                print(f"OK - {url}")
        except Exception as e:
            print(f"FAILED - {url}: {e}; bad response, failed parsing. skipping")
            continue

        get_data_from_log(j)

def get_data_from_log(j):
    nicks = dict(j['names']).items()
    teamRed = []
    teamBlu = []

    for k, v in nicks:
        if is_player_added(k) == False:
            player_list.append(player.createPlayer(k, v))
    
    #gameLength = int(j['length'])
    scoreRed = get_scores_from_data(j, 'Red')
    scoreBlu = get_scores_from_data(j, 'Blue')

    for i in j['players'].items():
        id = i[0]
        
def get_scores_from_data(j, team):
    for x in j["teams"].items():
        if x[0] == team:
            return x[1]["score"]

def is_player_added(id):
    for i in player_list:
        if i.id == id:
            return True
    return False

def end():
    for i in player_list:
        print(f"{i.id} - {i.nick}, elo: {i.elo}")