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

def playMusic(songObj: Song,ffmpeg,voice):
    global songNowPlaying
    songNowPlaying=songObj
    voice.play(FFmpegPCMAudio(songNowPlaying.urlYT,**ffmpeg), after=lambda x=None: checkQueue(queue1,voice))
    voice.is_playing()

async def joinVC(context,voice,channel):
    global diff_voice_chat
    diff_voice_chat=False
    if voice and voice.is_connected():
        if voice.channel==channel:
            pass
        else:
            await context.message.channel.send(f"Bot gra na innym czacie!")
            diff_voice_chat=True
    else:
        await channel.connect()

def makeEmbed(context, song:Song):
    myEmbed=discord.Embed(title=str(song.title),description=str(song.channel), color=color)
    myEmbed.add_field(name="Czas trwania:",value=durationFormat(song.duration),inline=True)
    myEmbed.add_field(name=str("Dodane przez: "),value=f"{context.message.author.mention}",inline=True) #do poprawy Requested by!
    myEmbed.add_field(name=str("Link:"),value=f"[URL]({song.webpage_url})",inline=True)
    return myEmbed



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

def checkQueue(queue1: Queue,voice):
    voice.stop()
    if queue1.queuelist!=[]:
        songObj=Song(queue1.queuelist[0].get("title"),queue1.queuelist[0].get("channel"),queue1.queuelist[0].get("duration"),queue1.queuelist[0].get("webpage_url"),queue1.queuelist[0].get("urlYT"))
        playMusic(songObj,ffmpeg_options,voice)
        songNowPlaying=songObj
        queue1.queuelist.pop(0)
        

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command(description="**Aktualna kolejka muzyki**")
    async def queue(self,context):
        queue1.listSongs()  
        embed=discord.Embed(title="Queue", color=color)
        if queue1.songNames==[]:
            embed.add_field(name="Kolejka jest pusta!",value="Dodaj piosenkę komendą !play",inline=False)
        else:
            for i in range(len(queue1.songNames)):
                nameVal=str(str(i+1)+'. '+str(queue1.songNames[i]))
                valVal=str(str(queue1.channelNames[i])+' ')
                embed.add_field(name=nameVal,value=valVal,inline=False)
        await context.message.channel.send(embed=embed)
    @commands.command(description="**Aktualnie grana muzyka**")
    async def nowplaying(self,context):
        myEmbed=makeEmbed(context, songNowPlaying)
        await context.message.channel.send("Aktualnie grane")        
        await context.message.channel.send(embed=myEmbed)
    @commands.command(description="**Włącza muzykę lub dodaj do kolejki**\nMożna podać URL z YT lub wpisać frazę do wyszukania\n\nPrzykład:\n**!play** linkYT\n**!play** daria laura")
    async def play(self,context, *searchYT:str):
        if not searchYT:
            await context.message.channel.send("Podaj link lub frazę!")
            return
        #print(context.author.voice.channel)
        if not context.author.voice:
            await context.message.channel.send("Nie jesteś na żadnym czacie głosowym!")
            return            
        searchYT=" ".join(searchYT)
        checkIfURL=searchYT.rfind("youtube.com/watch")
        channel=context.author.voice.channel
        global voice
        voice=get(self.bot.voice_clients,guild=context.guild)
        await joinVC(context,voice,channel)
        voice=get(self.bot.voice_clients,guild=context.guild)
        if diff_voice_chat==False:
            if not voice.is_playing():
                songObj=searchSong(searchYT,checkIfURL,ydl_options)
                playMusic(songObj,ffmpeg_options,voice)
                myEmbed=makeEmbed(context, songObj)
                await context.message.channel.send(embed=myEmbed)
            else:
                songObj=searchSong(searchYT,checkIfURL,ydl_options)            
                queue1.addSong(songObj)    
                await context.message.channel.send("Dodano do kolejki")
                myEmbed=makeEmbed(context,songObj)
                await context.message.channel.send(embed=myEmbed)
    @commands.command(desciption="Forceskip")
    async def forceskip(self,context):
        if context.message.author==context.guild.owner:
            if voice.is_playing():
                checkQueue(queue1,voice)
                myEmbed=makeEmbed(context,songNowPlaying)
                await context.message.channel.send("Pominięto piosenkę\n Aktualna piosenka")
                await context.message.channel.send(embed=myEmbed)
            else:
                await context.message.channel.send("Nic nie gra!")
        else:
            await context.message.channel.send("Nie masz uprawnień!")


async def setup(bot):
    await bot.add_cog(Music(bot))