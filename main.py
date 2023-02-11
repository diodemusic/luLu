#!usr/bin/env python3
# :3
import discord
import secret

intents = discord.Intents(messages=True)
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"<{client.user}> online.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(".hello") and message.content == ".hello":
        print(f"<{message.author}> {message.content}")
        await message.channel.send("hello :)")

client.run(secret.discordAPIKey)
