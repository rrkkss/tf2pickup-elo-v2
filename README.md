# python-tf2pickup-v2
because v1 straight up sucks

### dependencies
- python >= 3.0 version
- requests and xlsxwriter, both specified in .txt
- ``` pip install -r requirements.txt ```

### usage (config)
default value means that you can just press enter and get to the next one.

* Enter log title keyword, def(ault) 'tf2pickup.cz'
  - this is search phrase for logs. not a perfect solution as many games had problems launching through pickup's portal and they were simply hosted on random serveme serves.
* Enter wait time inbetween logs, def 0.4
  - numbers lower then 0.3 will get caught by ddos protection and that will result in a log not being processed. 0.4 is a safe value.
* Count bonus elo (extra elo points based on kills, deaths etc)? [y / n]; def y
  - you can add bonus elo to the standard one. it is based on formulas specified in:
  - https://github.com/rrkkss/tf2pickup-elo-v2/blob/f1f7e6eb299cbafb4924c135f8a68b2103cfb987/elo.py#L32
  - it was created to spread out players' elo rankings, effectively undermining bad players and boosting the good ones. 
* Count players' elo individually (player vs team [y]) or not (team vs team [n]); def n
  - player vs team
    - it uses your current elo against an averaged enemy team
  - team vs team
    - averages your team against the averaged enemy team
* Skip people with less then 5 games in the final log? [y / n]; def y
  - these people are still used in calculations but are skipped in the final print out, as their elo won't be much different from 1600. plus it's usually people from other countries who have played 1 - 2 games max.
* Set elo factor [number]; def 32
  - this is pretty much the maximum elo one can gain or lose. use 16 if you want the mge style elo.
* Export as a print into console or create an xlsx file with each player on a seperate sheet.

### problems / issues
- it is quite slow when working with large data sets.
- bonus elo was tailored to czech players, so it scales very poorly to larger groups (such as Poland or France). it needs to be reworked in that sense, but it is not such a big issue.
- currently it prints out (the result) as a list with objects, having multiple output types would be handy.
- etf2l api is cloudflared, so if you're one of those privacy aware peeps, you may not want to run the name conversion