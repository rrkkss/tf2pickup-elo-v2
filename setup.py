canAddBonusElo = True; countEloIndividually = False; canSkipShitters = True

def can_add_bonus_elo(input: str): # def true
    if input == 'n' or input == 'n':
        global canAddBonusElo
        canAddBonusElo = False

def count_elo_individually(input: str): # def false
    if input == 'y' or input == 'Y':
        global countEloIndividually
        countEloIndividually = True

def can_skip_shitters(input: str): # def true
    if input == 'n' or input == 'N':
        global canSkipShitters
        canSkipShitters = False