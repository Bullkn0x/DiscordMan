# bot.py
import os

import discord
from dotenv import load_dotenv
import random

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
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if '$FINDSTOCK' in message.content:
        try:
            ticker = message.content.split(' ')[1]
            await message.channel.send(ticker)
        except IndexError:
            await  message.channel.send('Please Input Ticker Symbol. Ex: $FINDSTOCK AAPL')



test = ['qi chen', 'rich duchin']
client.run(TOKEN)