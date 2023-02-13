#!usr/bin/env python3
# :3

from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import requests
import discord
from discord import app_commands

def configure():
    load_dotenv()

configure()

region = "euw1"
server_id = os.getenv("serverId")
discord_api_key = os.getenv("discordAPIKey")
riot_api_key = os.getenv("riotAPIKey")

def log(string):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(string)
    print(date_time, string)

def get_summoner_id(region, username, api_key):
    champion_id_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
    response = requests.get(champion_id_url)
    champion_id_json = response.json()
    summoner_id = champion_id_json["id"]
    return summoner_id

def get_active_game(region, username, api_key):
    encrypted_id = get_summoner_id(region, username, api_key)
    active_game_url = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{encrypted_id}?api_key={api_key}"
    response = requests.get(active_game_url)
    active_game_json = response.json()
    
    players = [[], []]
    for participant in active_game_json["participants"]:
        if participant["teamId"] == 100:
            players[0].append(participant["summonerName"])
        elif participant["teamId"] == 200:
            players[1].append(participant["summonerName"])
            
    return players

logging.basicConfig(filename='discord_bot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=server_id))
            self.synced = True
        log(f"Logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="ingame", description="Get active game stats", guild=discord.Object(id=server_id))
async def self(interaction: discord.Interaction, username: str):
    log(f"<{interaction.user}> /ingame {username}")
    
    try:
        players = get_active_game(region, username, riot_api_key)
    except KeyError as e:
        error_message = f"Player <{username}> is not in an active game."
        error_log_message = f"Error: KeyError: {e}. Sending: {error_message}"
        log(error_log_message)
        await interaction.response.send_message(error_message)
        return
    
    await interaction.response.send_message(f"""```team 1:
                                            player 1: {players[0][0]}
                                            player 2: {players[0][1]}
                                            player 3: {players[0][2]}
                                            player 4: {players[0][3]}
                                            player 5: {players[0][4]}```
                                            ```team 2:
                                            player 1: {players[1][0]}
                                            player 2: {players[1][1]}
                                            player 3: {players[1][2]}
                                            player 4: {players[1][3]}
                                            player 5: {players[1][4]}```""")

client.run(discord_api_key)
