import discord
from discord.ext import commands
import requests

TOKEN = 'token discord bot'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Escape from Tarkov"))
    print(f'Prisijungta kaip {bot.user}')

@bot.command()
async def kaina(ctx, *, item_name: str):
    query = """
    {
        items(name: "%s") {
            name
            avg24hPrice
        }
    }
    """ % item_name

    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    data = response.json()

    if 'errors' in data:
        await ctx.send('Įvyko klaida gaunant duomenis.')
        return

    items = data['data']['items']
    if not items:
        await ctx.send('Itemas nerastas.')
        return

    item = items[0]
    price = item['avg24hPrice']
    if price is None:
        await ctx.send(f"{item['name']} kaina nėra prieinama.")
    else:
        await ctx.send(f"{item['name']} vidutinė 24h kaina: {price} RUB")

bot.run(TOKEN)
