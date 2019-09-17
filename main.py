# bot.py
import os
import requests, json, discord
from dotenv import load_dotenv
import threading
import time
import datetime
from expiringdict import ExpiringDict


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
STOCK_TOKEN = os.getenv('STOCK_API_KEY')
CRYPTO_TOKEN = os.getenv('CRYPTO_API_KEY')
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

    if '$findstock' in message.content:
        # Remove whitespaces from input for exception handling
        ticker = message.content.replace(' ','')[10:]
        print(ticker, str(len(ticker)))
        if len(api_limit) < 5:
            try:
                stockinfo = getStockData(ticker)
                symbol, price, volume, \
                change, percent_change, \
                high, low= stockinfo['01. symbol'], stockinfo['05. price'],stockinfo['06. volume'], \
                           stockinfo['09. change'], stockinfo['10. change percent'], \
                           stockinfo['03. high'], stockinfo['04. low']
                if float(change) >= 0:
                    embed = discord.Embed(title="Stock", description=symbol, color=0x00ff00)
                else:
                    embed = discord.Embed(title="Stock", description=symbol, color=0xBF270C)

                embed.add_field(name="Price", value=f'${price}', inline=True)
                embed.add_field(name="Volume", value=volume, inline=True)
                embed.add_field(name="High", value=high, inline=True)
                embed.add_field(name="Low", value=low, inline=True)

                embed.add_field(name="Price Change", value=f'${change}', inline=True)
                embed.add_field(name="% Change", value=percent_change, inline=True)
                await message.channel.send(embed=embed)

            except KeyError:
                await message.channel.send('Invalid Stock Ticker. Ex: $FINDSTOCK AAPL')
        else:
            print(api_limit,'Failed')
            await message.channel.send('Too Many Calls Please Wait')

    if '$findcrypto' in message.content:

        cryptosymbol = message.content.replace(' ', '')[11:]
        print(cryptosymbol, str(len(cryptosymbol)))

        getCryptoData(cryptosymbol)

        embed = discord.Embed(title="Crypto", description=cryptosymbol, color=0x00ff00)
        embed.add_field(name="Time", value=1, inline=True)
        embed.add_field(name="Currency", value=2, inline=True)
        embed.add_field(name="Rate", value=3, inline=True)
        await message.channel.send(embed=embed)


api_limit = ExpiringDict(max_len=100, max_age_seconds=60)

def getCryptoData(symbol):
    url=f'http://rest-sandbox.coinapi.io/v1/exchangerate/{symbol}?apikey={CRYPTO_TOKEN}'
    response = requests.get(url)
    data = response.text
    print(data)


def getStockData(ticker):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=5min&apikey={STOCK_TOKEN}'
    response = requests.get(url)
    data = response.text
    json_data = json.loads(data)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    api_limit[st]=1
    print(api_limit, len(api_limit), 'Succeeded')
    return json_data['Global Quote']




client.run(TOKEN)
