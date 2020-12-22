import os
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import discord
import requests
from celery import Celery
import redis

app = Flask(__name__)
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'],
                CELERY_TASK_SERIALIZER="json")

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)

MY_APPLICATION_ID = 789179929979125821
CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"
BOT_TOKEN = os.environ['BOT_TOKEN']

interaction_token = []
players = []

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    json = request.json
    if json['type'] == InteractionType.APPLICATION_COMMAND:
        if not players:
            print("---------------EMPTY PLAYERS---------------")
            players.append(json['member']['user']['id'])
            interaction_token.append(json['token'])
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': json['member']['user']['id']
                }
            })
            # print(players)
        else:
            print("************PLAYERS********************")
            players.append(json['member']['user']['id'])
            # print(players)
            url = f"https://discord.com/api/v8/webhooks/{MY_APPLICATION_ID}/{interaction_token[0]}/messages/@original"
            headers = {"Authorization": f"Bot {BOT_TOKEN}"}
            json = {"content": " ".join(players)}
            r = requests.patch(url, headers=headers, json=json)
            # print(r)
            return jsonify({
                'type': InteractionResponseType.ACKNOWLEDGE
            })
