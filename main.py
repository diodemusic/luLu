#!usr/bin/env python3
# :3
import discord
import secret
from datetime import datetime

intents = discord.Intents(messages=True)
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} bot online.")

@client.event
async def on_message(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    print(f"{dt_string} <{message.author}> {message.content}")
    
    if message.author == client.user:
        return

    if message.content.startswith(".hello") and message.content == ".hello":
        await message.channel.send("hello :)")

client.run(secret.discordAPIKey)
