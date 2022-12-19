# bot.py
import discord
from discord.ext import commands
from discord.utils import get
from discord import TextChannel
import os
from dotenv import load_dotenv
import random
from classes import *
from music import Music
from games import Games


queue1=Queue()



color=0x00ff00


'''opcje wyszukiwania yt i grania muzyki'''






'''komendy i eventy'''
def run_discord_bot():
    
    '''Wywolanie bota'''
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client=commands.Bot(intents=intents,command_prefix='!')

    '''Wersja bota'''
    @client.command(name='version',help='Version of bot')
    async def version(context):
        myEmbed=discord.Embed(title="Current version",description="Version 1.0", color=color)
        myEmbed.add_field(name="Version:",value="v1.0",inline=False)
        
        await context.message.channel.send(embed=myEmbed)


    @client.event
    async def on_ready():
        await client.load_extension("music")
        await client.load_extension("games")
        print(f'{client.user} is running!')
    
    client.run(TOKEN)