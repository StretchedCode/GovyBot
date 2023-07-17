import requests, json


def getAnimeData(id: str):

    res = requests.get(f'https://api.jikan.moe/v4/anime?q={id}&sfw&limit=1')
    response = res.json()
    with open('data.json', '+a', encoding='utf-8') as dataFile:
        json.dump(response, dataFile, indent=4)

    return response