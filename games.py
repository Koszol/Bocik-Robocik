import discord
from discord.ext import commands
import random
from discord.utils import get
color=0x00ff00

def roll_number(*args): 
    '''Funkcja zwracająca losową liczbę'''
    len_of_args=len(args)
    if len_of_args==0:
        return str(random.randint(1,6))
    elif len_of_args==1:
        return str(random.randint(1,int(args[0])))
    elif len_of_args==2:
        print(args[0])
        print(args[1])
        if int(args[0])>int(args[1]):
            return str(random.randint(int(args[1]),int(args[0])))
        else:
            return str(random.randint(int(args[0]),int(args[1])))
    else:
        return 'Wrong number of arguments'

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command()
    async def roll(self,context, *args):
        myEmbed=discord.Embed(title="ROLLED:",description=roll_number(*args), color=color)
        myEmbed.add_field(name=str("Requested by: "),value=f"{context.message.author.mention}",inline=False)
        await context.message.channel.send(embed=myEmbed)   


    @commands.command()
    async def pingme(self,context):
        await context.message.channel.send(f"{context.message.author.mention}, dumb bitch!")

async def setup(bot):
    await bot.add_cog(Games(bot))
