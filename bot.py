# bot.py
import discord
from discord.ext import commands
from discord.utils import get
from discord import TextChannel
import os
from dotenv import load_dotenv
from classes import MyNewHelp
color=0x00ff00

'''komendy i eventy'''
def run_discord_bot():
    
    '''Wywolanie bota'''
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client=commands.Bot(intents=intents,command_prefix='!')
    client.help_command=MyNewHelp()
    @client.event
    async def on_ready():
        await client.load_extension("misc")
        await client.load_extension("music")
        await client.load_extension("games")
        print(f'{client.user} is running!')
    
    client.run(TOKEN)