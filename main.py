import os
import requests, json, discord
from dotenv import load_dotenv
import time
import datetime
from expiringdict import ExpiringDict

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
STOCK_TOKEN = os.getenv('STOCK_API_KEY')
CRYPTO_TOKEN = os.getenv('CRYPTO_API_KEY')
CRYPTO_NOMICS_TOKEN = os.getenv('CRYPTO_NOMICS_API_KEY')
client = discord.Client()

def getCryptoData(symbol):
    # coinapi=f'http://rest-sandbox.coinapi.io/v1/exchangerate/{symbol}/USD/?apikey={CRYPTO_TOKEN}'
    nomics=f'https://api.nomics.com/v1/currencies/ticker?key={CRYPTO_NOMICS_TOKEN}&ids={symbol}&interval=1d,30d&convert=USD&include-transparency=false'
    response = requests.get(nomics)
    data = response.text
    json_data = json.loads(data)
    return json_data[0]
    # return json_data


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

                colorformat = 0xBF270C
                diff='-'
                if float(change) > 0:
                    colorformat= 0x00ff00
                    diff='+'
                embed = discord.Embed(title="Stock", description=symbol, color=colorformat)

                embed.add_field(name="Price", value=f'${price}', inline=True)
                embed.add_field(name="Volume", value=volume, inline=True)
                embed.add_field(name="High", value=high, inline=True)
                embed.add_field(name="Low", value=low, inline=True)

                embed.add_field(name="Price Change", value=f'```diff\n{diff}${change}\n```', inline=True)
                embed.add_field(name="% Change", value=f'```diff\n{diff}{percent_change}\n```', inline=True)
                await message.channel.send(embed=embed)

            except KeyError:
                await message.channel.send('Invalid Stock Ticker. Ex: $FINDSTOCK AAPL')
        else:
            print(api_limit,'Failed')
            await message.channel.send('Too Many Calls Please Wait')

    if '$findcrypto' in message.content:

        cryptosymbol = message.content.replace(' ', '')[11:]
        symbol = cryptosymbol.upper()
        cryptoinfo = getCryptoData(symbol)
        name = cryptoinfo['name']
        rank = cryptoinfo['rank']
        # Pulls logo from online source with PNG because SVG is not compatible
        icon = f'https://coincodex.com/en/resources/images/admin/coins/{name}.png'

        time = cryptoinfo['price_date']

        # alter decimal based on price
        decimalcount=2
        if float(cryptoinfo['price']) < 1:
            decimalcount = 6

        price = round(float(cryptoinfo['price']), decimalcount)
        price_change = round(float(cryptoinfo['1d']['price_change']),decimalcount)
        percent_change = round(float(cryptoinfo['1d']['price_change_pct'])*100,2)
        embed = discord.Embed(title="Rank Coin Symbol", description=f'#{rank} {name} ({symbol})', color=0x00ff00)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Date", value=time, inline=True)
        embed.add_field(name="Price", value=f'${price}', inline=True)
        embed.add_field(name="Change (24 Hr)", value=f'${price_change}', inline=True)
        embed.add_field(name="% Change (24 Hr)", value=f'{percent_change}%', inline=True)
        await message.channel.send(embed=embed)

    if message.content == '!help':
        embed = discord.Embed(title="Help Menu", description='Here are a list of Commands and their uses', color=0x00ff00)
        embed.add_field(name="```$findcrypto [Symbol]```", value='This will return daily information for the coin')
        embed.add_field(name="```$findstock [Symbol]```", value='This will return daily information for the stock')
        embed.add_field(name="```!help```", value='A manual for all of the bot functions ')
        await message.channel.send(embed=embed)






api_limit = ExpiringDict(max_len=100, max_age_seconds=60)

if __name__ == '__main__':
    client.run(TOKEN)
