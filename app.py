from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import discord
import requests

app = Flask(__name__)

MY_APPLICATION_ID = 789179929979125821
CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"

players = []

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    json = request.json
    if json['type'] == InteractionType.APPLICATION_COMMAND:
        if not players:
            players.append(json['member']['user']['id'])
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': json['member']['user']['id']
                }
            })
        else:
            interaction_token = json['token']
            url = f"https://discord.com/api/v8/webhooks/application.id/{interaction_token}/messages/@original"
            content = " ".join(players)
            requests.patch(url, json=content)
            return jsonify({
                'type': InteractionResponseType.PONG
            })
