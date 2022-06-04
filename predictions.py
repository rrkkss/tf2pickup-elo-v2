def was_prediction_right(blu, red, bluWin, redWin):
    if blu > red and bluWin > redWin:
        return True
    elif blu > red and bluWin < redWin:
        return False
    elif blu < red and bluWin < redWin:
        return True
    elif blu < red and bluWin > redWin:
        return False
    elif blu == red and bluWin == redWin:
        return True
    elif blu == red and (bluWin > redWin or bluWin < redWin):
        return False
    elif (blu > red or blu < red) and bluWin == redWin:
        return False
    return False