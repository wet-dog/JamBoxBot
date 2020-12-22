import os
from flask import Flask, request, jsonify, session
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import discord
import requests

app = Flask(__name__)

MY_APPLICATION_ID = 789179929979125821
CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"
BOT_TOKEN = os.environ['BOT_TOKEN']

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# interaction_token = []
# players = []

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    json = request.json
    if json['type'] == InteractionType.APPLICATION_COMMAND:
        if 'interaction_token' not in session:
            print("---------------EMPTY PLAYERS---------------")
            # players.append(json['member']['user']['id'])
            session['interaction_token'] = json['token']
            session['players'] = [json['member']['user']['id']]
            # interaction_token.append(json['token'])
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': json['member']['user']['id']
                }
            })
            # print(players)
        else:
            print("************PLAYERS********************")
            # players.append(json['member']['user']['id'])
            session['players'].append(json['member']['user']['id'])
            # print(players)
            url = f"https://discord.com/api/v8/webhooks/{MY_APPLICATION_ID}/{session['interaction_token']}/messages/@original"
            headers = {"Authorization": f"Bot {BOT_TOKEN}"}
            json = {"content": " ".join(session['players'])}
            r = requests.patch(url, headers=headers, json=json)
            # print(r)
            return jsonify({
                'type': InteractionResponseType.PONG
            })
