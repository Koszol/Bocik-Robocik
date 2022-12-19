import discord
from discord.ext import commands
from classes import Queue,Song,durationFormat
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord import TextChannel

color=0x00ff00
queue1=Queue()

'''opcje wyszukiwania yt i grania muzyki'''
ydl_options={
    'format': 'bestaudio',
    'noplaylist':'True'
    }
ffmpeg_options={
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'}

def playMusic(songObj,ffmpeg,voice):
    global songNowPlaying
    songNowPlaying=songObj
    voice.play(FFmpegPCMAudio(songObj.urlYT,**ffmpeg), after=lambda x=None: checkQueue(queue1,voice))
    voice.is_playing()

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
def checkQueue(queue1,voice):
    if queue1.queuelist!=[]:
        songObj=Song(queue1.queuelist[0].get("title"),queue1.queuelist[0].get("channel"),queue1.queuelist[0].get("duration"),queue1.queuelist[0].get("webpage_url"),queue1.queuelist[0].get("urlYT"))
        playMusic(songObj,ffmpeg_options,voice)
        queue1.queuelist.pop(0)

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command()
    async def hello(self,context):
        await context.message.channel.send("Hello World!")
    @commands.command()
    async def queue(self,context):
        queue1.listSongs()  
        embed=discord.Embed(title="Queue", color=color)
        if queue1.songNames==[]:
            embed.add_field(name="Queue is empty!",value="Add song to queue with play command",inline=False)
        else:
            for i in range(len(queue1.songNames)):
                nameVal=str(str(i+1)+'. '+str(queue1.songNames[i]))
                valVal=str(str(queue1.channelNames[i])+' '+queue1.durationNames[i])
                embed.add_field(name=nameVal,value=valVal,inline=False)
        await context.message.channel.send(embed=embed)
    @commands.command()
    async def nowplaying(self,context):
        myEmbed=discord.Embed(title=str(songNowPlaying.title),description=str(songNowPlaying.channel), color=color)
        myEmbed.add_field(name="Duration:",value=durationFormat(songNowPlaying.duration),inline=True)
        myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=True)
        myEmbed.add_field(name=str("Link:"),value=f"[URL]({songNowPlaying.webpage_url})",inline=True)
        await context.message.channel.send("Now playing")        
        await context.message.channel.send(embed=myEmbed)
    @commands.command()
    async def play(self,context, *searchYT:str):
        if not searchYT:
            await context.message.channel.send("No link")
            return
        searchYT=" ".join(searchYT)
        checkIfURL=searchYT.rfind("https://")
        channel=context.author.voice.channel
        voice=get(self.bot.voice_clients,guild=context.guild)
        await joinVC(context,voice,channel)
        voice=get(self.bot.voice_clients,guild=context.guild)
        if not voice.is_playing():
            songObj=searchSong(searchYT,checkIfURL,ydl_options)
            #queue1=Queue(songObj.title,songObj.channel,songObj.duration,songObj.webpage_url,songObj.urlYT)

            playMusic(songObj,ffmpeg_options,voice)
            myEmbed=discord.Embed(title=str(songObj.title),description=str(songObj.channel), color=color)
            myEmbed.add_field(name="Duration:",value=durationFormat(songObj.duration),inline=True)
            myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=True)
            myEmbed.add_field(name=str("Link:"),value=f"[URL]({songObj.webpage_url})",inline=True)
            await context.message.channel.send(embed=myEmbed) 
        else:

            songObj=searchSong(searchYT,checkIfURL,ydl_options)            
            queue1.addSong(songObj.title,songObj.channel,songObj.duration,songObj.webpage_url,songObj.urlYT)    
            await context.message.channel.send("Added to queue")
            myEmbed=discord.Embed(title=str(songObj.title),description=str(songObj.channel), color=color)
            myEmbed.add_field(name="Duration:",value=durationFormat(songObj.duration),inline=True)
            myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=True)
            myEmbed.add_field(name=str("Link:"),value=f"[URL]({songObj.webpage_url})",inline=True)
            await context.message.channel.send(embed=myEmbed)

async def setup(bot):
    await bot.add_cog(Music(bot))