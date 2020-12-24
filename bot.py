import os
import requests
import discord

MY_APPLICATION_ID = 789179929979125821
GUILD_ID = 697583665118707757
BOT_TOKEN = os.environ['BOT_TOKEN']

url = f"https://discord.com/api/v8/applications/{MY_APPLICATION_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}"
}

json = {
    "name": "cum",
    "description": "Send cum",
    "options": []
}

r = requests.post(url, headers=headers, json=json)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_message_edit(before, after):
    # after = message
    # after.embeds
    # after.embeds[0].fields[-1].name
    # if message edit was by the bot
    if after.author == client.user:
        embed = after.embeds[0]
        field = embed.fields[0]
        players = field.value.split("\n")
        players = [x for x in players if x]
        player = players[-1]
        info = player.split(": ")
        user_id = player[0]
        print(user_id)
        user = client.get_user(user_id)

        await user.send('👀')


client.run(BOT_TOKEN)
