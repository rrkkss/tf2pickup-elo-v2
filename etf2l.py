import requests

def get_nick(id: str) -> str or Exception:
    try:
        var = requests.get(f"https://api.etf2l.org/player/{id}.json").json()
        return var["player"]["name"]
    except:
        # if conversion fails, nickname from pickup is used
        return None