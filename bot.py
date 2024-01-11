import discord
import environ
import requests
from discord.ext import commands

env = environ.Env()

API_TOKEN = env.str('DISCORD_RL_TRACKER_API_TOKEN')
RAPID_API_KEY = env.str('RAPID_API_KEY')

description = 'A Discord bot for checking Rocket League ranks using FastAPI'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',
                   description=description,
                   intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def ranks(ctx, username: str):
    '''Gets the ranks from a given user.'''

    url = f"https://rocket-league1.p.rapidapi.com/ranks/{username}"

    headers = {
        "User-Agent": "RapidAPI Playground",
        "Accept-Encoding": "identity",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "rocket-league1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    body = response.json()
    if response.status_code == 200:
        ''' Example response
        ```
        Duel (Ranked):      Diamond 1
        ```
        '''

        res = '```'
        for rank in body.get('ranks', {}):
            res += f"{rank.get('playlist')}:       {rank.get('rank')} ({rank.get('mmr')}mmr)"
        res += '```'

        await ctx.send(res)

    else:
        res = f"```{response.status_code}: {body.get('message', body)}```"
        await ctx.send(res)


bot.run(API_TOKEN)
