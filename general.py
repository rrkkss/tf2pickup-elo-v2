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
    isNumberValid = False

    if not is_number_valid(num):
        while isNumberValid == False:
            num = input(f"Not a valid number, enter a new one => ")
            if is_number_valid(num):
                isNumberValid = True
    
    return float(num)

def is_number_valid(num: any) -> bool:
    try:
        float(num)
        return True
    except:
        return False

def set_elo_factor(num: int) -> int:
    isValid = False

    while isValid == False:
        try:
            num = int(num)
            if num > 0:
                isValid = True
        except:
            num = input(f"Not a valid number, please enter a new one => ")

    return num