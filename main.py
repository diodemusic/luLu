import discord

intents = discord.Intents(messages=True)
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(".hello") and message.content == ".hello":
        print(f'message from {message.author} "{message.content}" recieved.')
        await message.channel.send("hello :)")

client.run("")
