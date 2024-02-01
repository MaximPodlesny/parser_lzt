import requests

headers = {
    'authority': 'forma.tinkoff.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    'origin': 'https://dolyame.ru',
    'referer': 'https://dolyame.ru/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

params = {
    'id': [
        'onepointone',
        'ivadesign',
        'gorkaoriginal',
        'cashenelle',
        'ivolga',
        'Murkott',
        'Monreve',
        'iamnotmaison',
        '3c3f5150-00c6-482d-887d-9bffc4559985',
        'sevenlabnyc',
        'martsevaya',
        'octagonshop',
        'shapewearstore',
        '2bac4075-e33c-4260-a39c-ff324a7a3fbe',
        'cosmomerch',
        'tefanorossi',
        'b6af1398-5aa2-40e4-a3a8-8a13dedd37a6',
        'saintsquad',
        '3f2b9305-9e5c-44ce-819e-ddba2ac39c2d',
        'tobewoman',
        'istok',
        'dd608e07-5a95-4259-9745-3723bc658270',
        'lamilami',
        'dussharussia',
        'hisoka',
        'furly',
        'Orrez Store',
        'handsrememberclothes',
        'santoriniatelier',
        'levitaciaco',
    ],
}

response = requests.get('https://forma.tinkoff.ru/api/bnpl/site/v1/get-partners', params=params, headers=headers)
print(*[f'{n} - {i["name"], i["shopURLWeb"]}' for n, i in enumerate(response.json())], sep='\n')