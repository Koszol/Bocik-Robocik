def durationFormat(duration):
    minutes=duration//60
    seconds=duration%60
    if seconds<=10:
        seconds=str("0"+str(seconds))
    return str(str(minutes)+":"+str(seconds))

class Song:
    def __init__(self,title,channel,duration,webpage_url,urlYT) -> None:
        self.title=title
        self.channel=channel
        self.duration=duration
        self.webpage_url=webpage_url
        self.urlYT=urlYT

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
    def listSongs(self):
        self.songNumber=[]
        self.songNames=[]
        self.channelNames=[]
        self.durationNames=[]
        for i in self.queuelist:
            self.songNames.append(i.get("title"))
            self.channelNames.append(i.get("channel"))
            self.durationNames.append(durationFormat(i.get("duration")))
