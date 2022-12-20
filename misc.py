import discord
from discord.ext import commands

color=0x00ff00

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command(description="**Aktualna wersja bota**")
    async def version(self,context):
        myEmbed=discord.Embed(title="Current version",description="Version 1.0", color=color)
        myEmbed.add_field(name="Version:",value="v1.0",inline=False)
        await context.message.channel.send(embed=myEmbed)

async def setup(bot):
    await bot.add_cog(Misc(bot))