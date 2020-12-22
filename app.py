import os
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import discord
import requests
from celery import Celery
import redis

app = Flask(__name__)

celery = Celery(app.name)
celery.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                   CELERY_RESULT_BACKEND=os.environ['REDIS_URL'],
                   CELERY_TASK_SERIALIZER="json")

r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)

MY_APPLICATION_ID = 789179929979125821
CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"
BOT_TOKEN = os.environ['BOT_TOKEN']

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    json = request.json
    if json['type'] == InteractionType.APPLICATION_COMMAND:
        if not r.exists("interaction_token"):
            print("---------------EMPTY PLAYERS---------------")
            r.set("interaction_token", json['token'])
            r.rpush("players", json['member']['user']['id'])
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': json['member']['user']['id']
                }
            })
            # print(players)
        else:
            print("************PLAYERS********************")
            r.rpush("players", json['member']['user']['id'])
            # print(players)
            interaction_token = r.get("interaction_token")
            url = f"https://discord.com/api/v8/webhooks/{MY_APPLICATION_ID}/{interaction_token[0]}/messages/@original"
            headers = {"Authorization": f"Bot {BOT_TOKEN}"}
            json = {"content": " ".join(r.get("players"))}
            req = requests.patch(url, headers=headers, json=json)
            # print(r)
            return jsonify({
                'type': InteractionResponseType.ACKNOWLEDGE
            })
