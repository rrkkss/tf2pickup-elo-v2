import general

wait = 0; search = ''
canAddBonusElo = True; countEloIndividually = False; canSkipShitters = True; etf2lNicks = True

def can_add_bonus_elo(input: str): # def true
    if input.lower() == 'n':
        global canAddBonusElo
        canAddBonusElo = False

def count_elo_individually(input: str): # def false
    if input.lower() == 'y':
        global countEloIndividually
        countEloIndividually = True

def init_setup(elo: object):
    global search; global wait
    search = input("\nEnter log title keyword, def 'tf2pickup.cz' => ") or 'tf2pickup.cz'
    wait = input("Enter wait time inbetween logs, def 0.4 => ") or 0.4
    wait = general.is_wait_number_valid(wait)
    can_add_bonus_elo(input("Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y => ") or 'y')
    count_elo_individually(input("Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n => ") or 'n')
    elo.eloFactor = general.set_elo_factor(input("Set elo factor -> max limit of elo change; def 32 => ") or 32)

def can_skip_shitters(input: str):
    if input.lower() == 'y':
        return True
    else:
        return False

def set_etf2l_nicks(input: str):
    global etf2lNicks
    if input.lower() != 'y':
        etf2lNicks = False

def check_export_method(inp: str) -> str:
    inp = inp.lower()
    if inp != 'print' and inp != 'xlsx':
        while True:
            inp = input(f"Not valid, choose again => ")
            if inp == 'print' or inp == 'xlsx':
                break
    return inp