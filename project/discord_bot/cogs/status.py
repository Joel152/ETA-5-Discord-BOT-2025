import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Set the bot's status when ready"""
        activity = discord.Activity(type=discord.ActivityType.watching, name="Tutorials")
        await bot.change_presence(status=discord.Status.online, activity=activity)

async def setup(bot):
    await bot.add_cog(Status(bot))
