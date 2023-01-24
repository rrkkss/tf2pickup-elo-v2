import parse
import results
import stats

def main():
    parse.init_parse()
    results.show_results(stats.playerList, parse.predictionFalse, parse.predictionRight, parse.canSkipShitters)

if __name__ == '__main__':
    main()
