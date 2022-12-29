import discord
from discord.ext import commands
from typing import Optional
color=0x00ff00

def durationFormat(duration):
    minutes=duration//60
    seconds=duration%60
    if seconds<=10:
        seconds=str("0"+str(seconds))
        return str(str(minutes)+":"+str(seconds))


class Song:
    def __init__(self,title,channel,duration,webpage_url,urlYT,requestPerson=None):
        self.title=title
        self.channel=channel
        self.duration=duration
        self.webpage_url=webpage_url
        self.urlYT=urlYT
        self.requestPerson=requestPerson

class Queue:
    def __init__(self) -> None:
        self.queuelist=[]
    def addSong(self,songAdd: Song):
        songToAdd={"title":songAdd.title,
        "channel": songAdd.channel,
        "duration":songAdd.duration,
        "webpage_url":songAdd.webpage_url,
        "urlYT":songAdd.urlYT
        }
        self.queuelist.append(songToAdd)
    def listSongs(self):
        self.songNames=[]
        self.channelNames=[]
        self.durationNames=[]
        for i in self.queuelist:
            self.songNames.append(i.get("title"))
            self.channelNames.append(i.get("channel"))
            #self.durationNames.append(durationFormat(i.get("duration")))
            

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page,color=color)
            await destination.send(embed=emby)