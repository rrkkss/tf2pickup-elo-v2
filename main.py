import parse
import results

def main():
    parse.init_parse()
    results.show_results(parse.playerList, parse.predictionFalse, parse.predictionRight, parse.canSkipShitters)

if __name__ == '__main__':
    main()
