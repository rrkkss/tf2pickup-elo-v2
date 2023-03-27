import parse
import results
import stats

def main():
    parse.init_parse()
    results.show_results(stats.playerList, stats.predictionFalse, stats.predictionRight)

if __name__ == '__main__':
    main()
