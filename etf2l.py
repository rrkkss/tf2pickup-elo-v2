import requests

def get_etf2l_nick(id: str) -> str or None:
    try:
        # for some fucking reason it doesn't return json, so that's that
        return requests.get(f"https://api.etf2l.org/player/{id}").content.decode('utf8').replace("'", '"').split('"name" : "')[1].split('"')[0]
    except:
        return None