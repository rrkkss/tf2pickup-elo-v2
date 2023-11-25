def was_prediction_right(blu: str, red: str, blu_win: float, red_win: float) -> bool:
    if (blu > red and blu_win > red_win) or (blu < red and blu_win < red_win) or (blu == red and blu_win == red_win):
        return True
    elif (blu > red and blu_win < red_win) or (blu < red and blu_win > red_win) or (blu == red and (blu_win > red_win or blu_win < red_win)) or ((blu > red or blu < red) and blu_win == red_win):
        return False
    return False