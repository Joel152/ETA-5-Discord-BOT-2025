import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Set the bot's status when ready"""
        activity = discord.Game(name="Managing the Community")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        self.bot.logger.info(f"Bot status set to: Managing the Community")

async def setup(bot):
    await bot.add_cog(Status(bot))
