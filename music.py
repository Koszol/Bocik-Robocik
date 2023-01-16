import discord
from discord.ext import commands, tasks
from classes import Queue,Song,durationFormat
from discord.utils import get
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord import TextChannel
from math import ceil
import textwrap

color=0x00ff00
queue1=Queue()
global skipCount
skipCount=0
global disconnectCheck
disconnectCheck=False
global voice
voice=None
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
    global skipCount
    skipCount=0

def makeEmbed(context, songNow:Song):
    myEmbed=discord.Embed(title=str(songNow.title),description=str(songNow.channel), color=color)
    myEmbed.add_field(name="Długość:",value=durationFormat(songNow.duration),inline=True)
    #myEmbed.add_field(name=str("Dodane przez: "),value=f"{context.message.author.mention}",inline=True)
    myEmbed.add_field(name=str("Link:"),value=f"[URL]({songNow.webpage_url})",inline=True)
    return myEmbed    


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
        queue1.queuelist.pop(0)    
        playMusic(songObj,ffmpeg_options,voice)

def addPlaylistToQueue(playlist: dict):
    for video in playlist['entries']:
        songToAdd=Song(video['title'],video['channel'],video['duration'],video['webpage_url'],video['url'])
        queue1.addSong(songToAdd)
    print("Done!")


class Music(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.disconnect.start()

    '''Odpowiada za wyjscie z czatu głosowego'''
    @tasks.loop(seconds=5.0)
    async def disconnect(self):
        if voice is None:
            return
        else:
            if not voice.is_playing() and voice.is_connected():
                await voice.disconnect()
                global songNowPlaying
                songNowPlaying=None

    @commands.command(description="**Aktualna kolejka muzyki**")
    async def queue(self,context):
        queue1.listSongs()  
        embed=discord.Embed(title="Kolejka", color=color)
        if queue1.songNames==[]:
            embed.add_field(name="Kolejka jest pusta!",value="Dodaj piosenkę za pomocą komendy !play",inline=False)
        else:
            for i in range(len(queue1.songNames)):
                nameVal=str(str(i+1)+'. '+str(queue1.songNames[i]))
                valVal=str(str(queue1.channelNames[i])+' '+queue1.durationNames[i])
                embed.add_field(name=nameVal,value=valVal,inline=False)
        await context.message.channel.send(embed=embed)
    @commands.command(description="**Aktualnie grana muzyka**")
    async def nowplaying(self,context):
        if songNowPlaying==None:
            myEmbed=discord.Embed(title="Nic aktualnie nie gra!",description="Dodaj piosenkę za pomocą komendy !play",color=color)
        else:
            myEmbed=makeEmbed(context,songNowPlaying)
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
        print(searchYT)
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
                await context.message.channel.send("Aktualnie grane")
                myEmbed=makeEmbed(context,songObj)
                await context.message.channel.send(embed=myEmbed)
            else:
                songObj=searchSong(searchYT,checkIfURL,ydl_options)            
                queue1.addSong(songAdd=songObj)    
                await context.message.channel.send("Dodano do kolejki")
                myEmbed=makeEmbed(context,songObj)
                await context.message.channel.send(embed=myEmbed)
    @commands.command(description="**Dodaje całą playlistę**\nPodaj link do playlisty lub utworu na playliście\nPlaylista zostanie dodana do kolejki od pierwszego utworu")
    async def playlist(self, context, searchYT:str):
        if not searchYT:
            await context.message.channel.send("Podaj link do playlisty!")
            return     
        if not context.author.voice:
            await context.message.channel.send("Nie jesteś na żadnym czacie głosowym!")
            return
        checkIfURL=searchYT.rfind("youtube.com/")
        if checkIfURL==-1:
            await context.message.channel.send("Nieprawidłowy link!")
            return
        channel=context.author.voice.channel
        global voice
        voice=get(self.bot.voice_clients,guild=context.guild)
        await joinVC(context,voice,channel)
        voice=get(self.bot.voice_clients,guild=context.guild) 
        if diff_voice_chat==False:
            ydl_opt_playlist={
            'format': 'bestaudio',
            'quiet': 'True',
            'ignoreerrors': 'True'
            }
            with YoutubeDL(ydl_opt_playlist) as ydl:
                url=searchYT
                info=ydl.extract_info(url,download=False)  
                #print(playlist_dict['entries'])
                if not voice.is_playing():
                    songObj=Song(info['entries'][0]['title'],info['entries'][0]['channel'],info['entries'][0]['duration'],info['entries'][0]['webpage_url'],info['entries'][0]['url'])   
                    playMusic(songObj,ffmpeg_options,voice)
                    await context.message.channel.send("Aktualnie grane")
                    myEmbed=makeEmbed(context,songObj)
                    await context.message.channel.send(embed=myEmbed)
                    print(type(info["entries"]))
                    info['entries'].pop(0)                                    
                    addPlaylistToQueue(info)
                else:
                    addPlaylistToQueue(info)

    @commands.command(description="**Pomija aktualną piosenkę**\nTej komendy może użyć tylko właściciel serwera")
    async def forceskip(self,context):
        if context.message.author==context.guild.owner:
            voice.stop()
            await context.message.channel.send("Pominięto")
        else:
            await context.message.channel.send("Nie masz uprawnień!")
    
    @commands.command(description="**Zagłosuj na pominięcie utworu**\nZagłosować musi ponad połowa osób")
    async def skip(self,context):
        if not context.author.voice.channel:
            await context.message.channel.send("Nie jesteś na żadnym kanale!")
            return
        channel=context.author.voice.channel
        if voice.channel!=channel:
            await context.message.channel.send("Nie jesteś na tym samym czacie głosowym co bot!")
            return
        global skipCount
        skipCount+=1
        number_of_users=ceil(len(channel.members)-1)
        myEmbed=discord.Embed(title="Skip vote",description=f"Liczba osób na czacie: {len(channel.members)}", color=color)
        myEmbed.add_field(name="Vote status:",value=f"{skipCount}/{number_of_users}")
        await context.message.channel.send(embed=myEmbed)
        if(skipCount>=number_of_users):
            voice.stop()
            await context.message.channel.send("Pominięto")

async def setup(bot):
    await bot.add_cog(Music(bot))