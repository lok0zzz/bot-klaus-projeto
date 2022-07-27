import requests 
import constants as keys
 # League of Legends id: 5
match_url = 'https://www.rivalry.com/pt/match/league-of-legends/china-lpl/639218-lgd-vs-team-we'
#            www.rivalry.com/match/league-of-legends/china-lpl/639218-lgd-vs-team-we

try:
    resposta_games = requests.get(keys.GAMES_URL)
    resposta_games_dic = resposta_games.json()
    matches = resposta_games_dic['data']['matches']
except (requests.exceptions.RequestException) as e:
    print('Error getting matches')


for match in matches:
    if match_url[26:] in match['url']:
        print('ACHOU')
