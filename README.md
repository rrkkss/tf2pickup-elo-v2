# python-tf2pickup-v2
because v1 was quite bad

### dependencies
- python >= 3.0 version
- ``` pip install -r requirements.txt ```

### usage (config)
default value means that you can just press enter and get to the next one

* Enter log title keyword, def(ault) 'tf2pickup.cz'
  - this is search phrase for logs. not a perfect solution as many games had problems launching through pickup's portal and they were simply hosted on random serveme serves
* Enter wait time inbetween logs, def 0.4
  - numbers lower then 0.3 will get caught by ddos protection and that will result in a log not being processed. 0.4 is a safe value
* Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y
  - you can add bonus elo to the standard one. it is based on formulas specified in:
  - https://github.com/rrkkss/tf2pickup-elo-v2/blob/f1f7e6eb299cbafb4924c135f8a68b2103cfb987/elo.py#L32
  - it was created to spread out players' elo rankings, effectively undermining bad players and boosting the good ones
* Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n
  - player vs team
    - it uses your current elo against an averaged enemy team
  - team vs team
    - averages your team against the averaged enemy team
* Skip people with less then 5 games in the final log? [y / n]; def y
  - these people are still used in calculations but are skipped in the final print out, as their elo won't be much different from 1600. Plus it's usually people from other countries who have played 1 - 2 games at best
* Set elo factor [number]; def 32
  - this is pretty much the maximum elo one can gain or lose. Use 16 if you want the mge style elo.
* Export as a print into the console or create an xlsx file with each player as a seperate sheet.

### problems / issues
- it is quite slow when working with large data sets.
- bonus elo was tailored to czech players, so it scales very poorly to larger groups (such as Poland or France). It needs to be reworked in that sense, but it is not such a big issue
- ETF2L's API is **cloudflared**
