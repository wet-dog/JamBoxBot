from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType

app = Flask(__name__)

CLIENT_PUBLIC_KEY = "5c014e0bf7dec5d459505af626f181d3ff246a34a10faa6a9dd6a2e29613888f"

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    if request.json['type'] == InteractionType.APPLICATION_COMMAND:
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Hello world'
            }
        })
