import parse
import results

def main():
    parse.get_logs()
    results.show_results(parse.playerList, parse.predictionFalse, parse.predictionRight, parse.canSkipShitters)

if __name__ == '__main__':
    main()
