def compare_string(str1: str, str2: str) -> bool:
    if str1 == str2:
        return True
    return False

def get_winning_team(red: str, blu: str) -> str:
    if blu > red:
        return 'Blue'
    elif blu < red:
        return 'Red'
    else:
        return 'draw'

def is_wait_number_valid(num: float) -> float:
    is_number_valid = False

    if not is_float_valid(num):
        while is_number_valid == False:
            num = input("Not a valid number, enter a new one => ")
            if is_float_valid(num):
                is_number_valid = True
    
    return float(num)

def is_float_valid(num: any) -> bool:
    try:
        float(num)
        return True
    except:
        return False

def set_elo_factor(num: int) -> int:
    is_valid = False

    while is_valid == False:
        try:
            num = int(num)
            if num > 0:
                is_valid = True
        except:
            num = input("Not a valid number, please enter a new one => ")

    return num

def remove_invalid_chars(inp: str) -> str:
    word = []
    chars = ['[', ']', ':', '*', '?', '/', '\\']
    for char in inp:
        if char not in chars:
            word.append(char)

    return ''.join(str(v) for v in word)