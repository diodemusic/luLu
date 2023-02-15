#!usr/bin/env python3
# :3

from dotenv import load_dotenv
import os
import logging
import discord
from discord import app_commands
import math
import cassiopeia as cass
from tabulate import tabulate

def configure():
    load_dotenv()

configure()

server_id = os.getenv("serverId")
discord_api_key = os.getenv("discordAPIKey")
riot_api_key = os.getenv("riotAPIKey")
cass.set_riot_api_key(riot_api_key)

def get_game(region, username):
    summoner = cass.Summoner(region=region, name=username)
    active_game = summoner.current_match()

    stats = []

    for participant in active_game.participants:
        participant_stats = {}
        try:
            league_entries = participant.summoner.league_entries.fives # todo add to_json() from json module
            # print(league_entries)
        except:
            participant_stats["player"] = participant.summoner.name
            participant_stats["team"] = participant.side.name
            participant_stats["rank"] = "N/A"
            participant_stats["winrate"] = "N/A"
            stats.append(participant_stats)
            continue
        
        total_games_played = league_entries.wins + league_entries.losses
        winrate = math.floor(round((league_entries.wins / total_games_played) * 100))
        
        participant_stats["player"] = participant.summoner.name
        participant_stats["team"] = participant.side.name
        participant_stats["rank"] = f"{league_entries.tier.name} {league_entries.division} {league_entries.league_points}lp"
        participant_stats["winrate"] = f"{winrate}%"
        participant_stats["games_played"] = total_games_played
        participant_stats["hot_streak"] = league_entries.hot_streak
        # participant_stats["promos"] = league_entries.promos
        participant_stats["veteran"] = league_entries.veteran
        
        stats.append(participant_stats)

    return stats

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
        logging.info(f"Logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="ingame", description="Get active game stats", guild=discord.Object(id=server_id))
async def self(interaction: discord.Interaction, username: str):
    logging.info(f"<{interaction.user}> /ingame {username}")
    
    try:
        stats = get_game("EUW", username)
    except Exception as err:
        logging.error(f"Error: {err}.")
        await interaction.response.send_message(f"Error: {err}.")
        return
    
    table = tabulate(stats, headers="keys", tablefmt="psql")
    
    try:
        await interaction.response.send_message(f"```{table}```")
    except Exception as err:
        logging.error(f"Error: {err}")

client.run(discord_api_key)
