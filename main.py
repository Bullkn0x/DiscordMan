# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        print (guild.name, guild.id)
    print(f'{client.user} has connected to Discord!')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
client.run(TOKEN)