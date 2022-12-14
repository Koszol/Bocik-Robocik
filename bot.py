# bot.py
import discord
import responses
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord import TextChannel
import random

global voice

global color
color=0x00ff00

class Song:
    def __init__(self,title,channel,duration,webpage_url,urlYT) -> None:
        self.title=title
        self.channel=channel
        self.duration=duration
        self.webpage_url=webpage_url
        self.urlYT=urlYT

def durationFormat(duration):
    minutes=duration//60
    seconds=duration%60
    if seconds<=10:
        seconds=str("0"+str(seconds))
    return str(str(minutes)+":"+str(seconds))

'''class Queue():
    def __init__(self, title, channel, duration, webpage_url, urlYT) -> None:
        super().__init__(title, channel, duration, webpage_url, urlYT)
        self.songToAdd={"title":self.title,
        "channel": self.channel,
        "duration":self.duration,
        "webpage_url": self.webpage_url,
        "urlYT":self.urlYT}
        self.queuelist=[self.songToAdd]
    def addSong(self,title, channel, duration, webpage_url, urlYT):
        songToAdd={"title":title,
        "channel": channel,
        "duration":duration,
        "webpage_url":webpage_url,
        "urlYT":urlYT
        }
        self.queuelist.append(songToAdd)
        return self.queuelist'''

class Queue:
    def __init__(self) -> None:
        self.queuelist=[]
    def addSong(self,title, channel, duration, webpage_url, urlYT):
        songToAdd={"title":title,
        "channel": channel,
        "duration":duration,
        "webpage_url":webpage_url,
        "urlYT":urlYT
        }
        self.queuelist.append(songToAdd)

queue1=Queue()

def searchSong(searchYT,checkIfURL,ydl_options):
    with YoutubeDL(ydl_options) as ydl:
        if checkIfURL==-1:
            search_opt="ytsearch:{}"
            search_txt=search_opt.format(searchYT)
            info=ydl.extract_info(search_txt, download=False)
            url=info['entries'][0]['url']
            return Song(info['entries'][0]['title'],info['entries'][0]['channel'],info['entries'][0]['duration'],info['entries'][0]['webpage_url'],info['entries'][0]['url'])                
        else:
            url=searchYT
            info=ydl.extract_info(url,download=False)
            return Song(info['title'],info['channel'],info['duration'],info['webpage_url'],info['url'])    


async def joinVC(context,voice,channel):
    if voice and voice.is_connected():
        if voice.channel==channel:
            #await context.message.channel.send(f"I'm already here!")
            pass
        else:
            await voice.disconnect()
            await context.message.channel.send(f"Changing voice channel to {channel}")
            await channel.connect()
    else:
        await channel.connect()

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
        myEmbed=discord.Embed(title="Current version",description="Version 1.0", color=color)
        myEmbed.add_field(name="Version:",value="v1.0",inline=False)
        
        await context.message.channel.send(embed=myEmbed)

    '''Losowanie liczby'''
    @client.command(name='roll')
    async def roll(context, *args):
        myEmbed=discord.Embed(title="ROLLED:",description=roll_number(*args), color=color)
        myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=False)
        await context.message.channel.send(embed=myEmbed)   

    '''Pinguje autora''' 
    @client.command(name='pingme')
    async def pingme(context):
        await context.message.channel.send(f"{context.message.author.mention}")
    
    '''Obsluga voice-chatu'''
    @client.command(name="join")
    async def join(context):
        channel=context.author.voice.channel
        voice=get(client.voice_clients,guild=context.guild)
        await joinVC(context,voice,channel)

    @client.command(name="disconnect")
    async def disconnect(context):
        voice=get(client.voice_clients,guild=context.guild)         # bierze informacje o voice chacie
        await voice.disconnect()
    

    @client.command(name="play")
    async def play(context, *searchYT:str):
        if not searchYT:
            await context.message.channel.send("No link")
            return
        searchYT=" ".join(searchYT)
        checkIfURL=searchYT.rfind("https://")
        channel=context.author.voice.channel
        voice=get(client.voice_clients,guild=context.guild)
        await joinVC(context,voice,channel)
        ydl_options={
            'format': 'bestaudio',
            'noplaylist':'True'
            }
        ffmpeg_options={
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'}
        voice=get(client.voice_clients,guild=context.guild)
        if not voice.is_playing():
            song1=searchSong(searchYT,checkIfURL,ydl_options)
            #queue1=Queue(song1.title,song1.channel,song1.duration,song1.webpage_url,song1.urlYT)
            voice.play(FFmpegPCMAudio(song1.urlYT,**ffmpeg_options))
            voice.is_playing()
            myEmbed=discord.Embed(title=str(song1.title),description=str(song1.channel), color=color)
            myEmbed.add_field(name="Duration:",value=durationFormat(song1.duration),inline=True)
            myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=True)
            myEmbed.add_field(name=str("Link:"),value=f"[URL]({song1.webpage_url})",inline=True)
            await context.message.channel.send(embed=myEmbed) 
        else:
            '''dodanie do kolejki'''
            song1=searchSong(searchYT,checkIfURL,ydl_options)            
            queue1.addSong(song1.title,song1.channel,song1.duration,song1.webpage_url,song1.urlYT)    
            await context.message.channel.send("Added to queue")
            myEmbed=discord.Embed(title=str(song1.title),description=str(song1.channel), color=color)
            myEmbed.add_field(name="Duration:",value=durationFormat(song1.duration),inline=True)
            myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=True)
            myEmbed.add_field(name=str("Link:"),value=f"[URL]({song1.webpage_url})",inline=True)
            await context.message.channel.send(embed=myEmbed)
    '''wyswietlenie kolejki'''
    @client.event
    async def on_ready():
        print(f'{client.user} is running!')

    client.run(TOKEN)