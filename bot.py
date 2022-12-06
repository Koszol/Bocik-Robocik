# bot.py
import discord
import responses
from discord.ext import commands
from discord.utils import get
import random

'''
async def send_message(message, user_message,username, is_private):
    try:
        response = responses.get_response(user_message,username)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)
'''

def roll_number(*args): 
    '''Funkcja zwracająca losową liczbę'''
    len_of_args=len(args)
    if len_of_args==0:
        return str(random.randint(1,6))
    elif len_of_args==1:
        return str(random.randint(1,int(args[0])))
    elif len_of_args==2:
        if args[0]>args[1]:
            return str(random.randint(int(args[1]),int(args[0])))
        else:
            return str(random.randint(int(args[0]),int(args[1])))
    else:
        return 'Wrong number of arguments'



def run_discord_bot():

    '''Wywolanie bota'''
    TOKEN = 'MTA0Nzk5MjU1NDM5NTgxMTk1Mg.GtSoze.1Ftqn8-m0E5neMWUOWHMkOPdXMjXrchPJsLqUU'
    intents = discord.Intents.default()
    intents.message_content = True
    client=commands.Bot(intents=intents,command_prefix='!')

    '''Wersja bota'''
    @client.command(name='version',help='Version of bot')
    async def version(context):
        myEmbed=discord.Embed(title="Current version",description="Version 1.0", color=0x00ff00)
        myEmbed.add_field(name="Version:",value="v1.0",inline=False)
        
        await context.message.channel.send(embed=myEmbed)

    '''Losowanie liczby'''
    @client.command(name='roll')
    async def roll(context, *args):
        myEmbed=discord.Embed(title="ROLLED:",description=roll_number(*args), color=0x00ff00)
        myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=False)
        await context.message.channel.send(embed=myEmbed)   

    '''Pinguje autora''' 
    @client.command(name='pingme')
    async def pingme(context):
        await context.message.channel.send(f"{context.message.author.mention}")
    
    '''Obsluga voice-chatu'''
    @client.command(name="join")
    async def join(context):
        global voice
        channel=context.author.voice.channel
        voice=get(client.voice_clients,guild=context.guild)
        if voice and voice.is_connected():
            if voice.channel==channel:
                await context.message.channel.send(f"I'm already here!")
            else:
                await voice.disconnect()
                await context.message.channel.send(f"Changing voice channel to {channel}")
                await channel.connect()
        else:
            await channel.connect()
    
    @client.command(name="disconnect")
    async def disconnect(context):
        voice=get(client.voice_clients,guild=context.guild)         # bierze informacje o voice chacie
        await voice.disconnect()
    
    '''
    @client.command()
    async def help(context):
        help_text=open('help.txt',mode='r',encoding='utf-8')
        EmbedChannel=discord.Embed(title="Help sent",description='Check your DMs!' ,color=0x00ff00)
        EmbedChannel.add_field(name=str(""),value=f"{context.message.author.mention}",inline=False)
        EmbedUser=discord.Embed(title="Help:",description='help_text' ,color=0x00ff00)
        await context.message.author.send(help_text)
        await context.message.channel.send(embed=EmbedChannel)
        help_text.close()
    '''
    
    @client.event
    async def on_ready():
        print(f'{client.user} is running!')
        #general_channel=client.get_channel(1047996650175606797)
        #await general_channel.send('Hello!')

    '''
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return


        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        
        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message,username, is_private=True)
        else:
            await send_message(message, user_message,username, is_private=False)
        await client.process_commands(message)
    '''
    client.run(TOKEN)