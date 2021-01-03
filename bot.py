import os
import io
import requests
import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

cred = credentials.Certificate('C:\jambox-566ec-firebase-adminsdk-zag0d-179773188a.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'jambox-566ec.appspot.com'
})

db = firestore.client()

bucket = storage.bucket()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Checking for images in DM
    if isinstance(message.channel, discord.DMChannel):
        if message.attachments:
            for attachment in message.attachments:
                # Check if the attachment is an image/ video
                if attachment.width:
                    image = await attachment.to_file()
                    filename = str(message.author.id) + image.filename 
                    image = image.fp
                    print(attachment.filename)
                    print(filename)
                    blob = bucket.blob(filename)
                    blob.upload_from_file(image)

                    players = db.collection("players")
                    player = players.document(f"{message.author.id}")
                    player.set({
                        "id": f"{message.author.id}"
                    })
                    player_images = player.collection("images")
                    # player_images = players.document(f"{message.author.id}").collection("images")
                    player_images.document().set({
                        "name": f"{filename}"
                    })

    if message.content.startswith('$images'):
        print("images")
        images = db.collection_group("images").stream()
        names = []
        for image in images:
            print(f'{image.id} => {image.to_dict()}')
            names.append(image.to_dict()["name"])
            await message.channel.send(f'{image.id} => {image.to_dict()}')

    if message.content.startswith("$image"):
        blob = bucket.blob("175959993420349440masternacho.jpg")
        f = blob.download_as_bytes()
        # f = io.BytesIO(f)
        with io.BytesIO(f) as f:
                image = discord.File(f, "175959993420349440masternacho.jpg")
                await message.channel.send(file=image)

@client.event
async def on_message_edit(before, after):
    # after = message
    # after.embeds
    # after.embeds[0].fields[-1].name
    # if message edit was by the bot

    # replace redis with an entry in firestore?
    # or was firestore unnecessarsy?

    if after.author == client.user:
        embed = after.embeds[0]
        field = embed.fields[0]
        players = field.value.split("\n")
        players = [x for x in players if x]
        num_players = len(players)
        player = players[-1]
        info = player.split(": ")
        user_id = info[0]
        print(user_id)
        user = client.get_user(int(user_id))


        prev_players = before.embeds[0].fields[0].value.split("\n")
        prev_players = len([x for x in prev_players if x])
        if num_players != prev_players:
            await user.send('👀')

        prev_players = num_players


client.run(BOT_TOKEN)
