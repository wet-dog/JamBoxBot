import os
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import discord
import requests
from celery import Celery
import redis
import json

app = Flask(__name__)

celery = Celery(app.name)
celery.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                   CELERY_RESULT_BACKEND=os.environ['REDIS_URL'],
                   CELERY_TASK_SERIALIZER="json")

r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
r.flushdb()

MY_APPLICATION_ID = 789179929979125821
CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"
BOT_TOKEN = os.environ['BOT_TOKEN']

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    data = request.json
    if data['type'] == InteractionType.APPLICATION_COMMAND:
        discord_id = data['member']['user']['id']
        game_name = data['data']['options'][0]['value']
        if not r.exists("interaction_token"):
            r.set("interaction_token", data['token'])
            r.hsetnx("players", discord_id, game_name)

            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': data['member']['user']['id']
                }
            })
        else:
            interaction_token = r.get("interaction_token")
            url = f"https://discord.com/api/v8/webhooks/{MY_APPLICATION_ID}/{interaction_token}/messages/@original"

            r.hsetnx("players", discord_id, game_name)

            headers = {"Authorization": f"Bot {BOT_TOKEN}"}
            content = r.hgetall("players")
            data = {"content": json.dumps(content)}
            requests.patch(url, headers=headers, json=data)
            
            return jsonify({
                'type': InteractionResponseType.ACKNOWLEDGE
            })
