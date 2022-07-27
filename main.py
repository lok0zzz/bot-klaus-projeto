from telegram import Update
import constants as keys
from telegram.ext import *
import requests

print("\n\n\n\n\n\n\n\n BOT INICIADO \n\n\n\n\n\n\n\n")

# Functions
def get_all_games():
    all_games_awsner = requests.get(keys.GAMES_URL)
    all_games_dic = all_games_awsner.json()
    games = all_games_dic['data']['matches']
    if all_games_awsner.status_code != 200:
        Update.message.reply_text('ERRO DE REQUISIÇÃO (possivelmente muitas requisições ou NOTFOUND')
    return games

def find_match_id_by_url(url, matches):
    for match in matches:
        if url[26:] in match['url']:
            print('FIND')
            return match['id']

def find_match_data(id):
    match_found = requests.get(f'https://www.rivalry.com/api/v1/matches/{id}')
    if match_found.status_code != 200:
        Update.message.reply_text('ERRO DE REQUISIÇÃO (possivelmente muitas requisições ou NOTFOUND')
    data_from_match = match_found.json()
    return data_from_match

# Commands.
def startCommand(update, context):
    update.message.reply_text(
'''
Comandos:
/win APOSTAR NA VITÓRIA DE X TIME.
''')

def winCommand(update, context):
    # update.message.reply_text(f'ARG1 = {context.args[0]} | ARG2 = {context.args[1]}')
    if len(context.args) != 3:
        update.message.reply_text('Por favor, use: /win [VENCEDOR] [QUANTIDADE DE UNIDADES] [LINK]')
    else:
        try:
            all_game_matches = get_all_games()
            match_id = find_match_id_by_url(context.args[2], all_game_matches)
            data = find_match_data(match_id)
            
            competitor_1 = data['data']['competitors'][0]['name']
            competitor_2 = data['data']['competitors'][1]['name']
            camp_name = data['data']['tournament']['name']
            url = context.args[2]
            odd_1 = data['data']['markets'][-1]['outcomes'][0]['odds']
            odd_2 = data['data']['markets'][-1]['outcomes'][1]['odds']
        except (requests.exceptions.RequestException) as e:
            update.message.reply_text(f'Erro ao procurar os jogos. Contate o desenvolvedor.\n Erro: {e}')
            return
            
        except Exception as e:
            update.message.reply_text(f'ERRO, favor entre em contato com o desenvolvedor.\nErro: {e}')
            return
            

        if context.args[0] == '1':
            winner = competitor_1
        elif context.args[0] == '2':
            winner = competitor_2
        else:
            update.message.reply_text('''
Lado não encontrado, tente usar:
[1] Para o primeiro competidor.
[2] Para o segundo competidor.
                                      
Caso o erro continue, contate o desenvolvedor.''')
            return
        update.message.reply_text(
            f'''
🚨 ATENÇÃO, NOVA APOSTA 🚨
            
[{odd_1}] {competitor_1} X {competitor_2} [{odd_2}]

Nome do campeonato: {camp_name}

Votar em: {winner}
Valor: {context.args[1]}u
            
            
{url}
            
            '''
        )
        
# Run the bot.
def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler(["start", "help"], startCommand))
    dp.add_handler(CommandHandler("win", winCommand))


    # Run the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
