"""
Handles user reports and incident management
"""
import discord
from discord.ext import commands
from ..config import REPORTS_CHANNEL_ID
from ..utils.embeds import create_report_embed

class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx, member: discord.Member, *, reason: str):
        """Report a user for breaking rules"""
        # Delete the command message to keep it private
        try:
            await ctx.message.delete()
        except:
            pass

        # Send confirmation to the reporter
        try:
            await ctx.author.send("✅ Your report has been submitted to the moderators. Thank you for helping keep the server safe!")
        except discord.Forbidden:
            pass

        # Send report to moderators
        reports_channel = ctx.guild.get_channel(REPORTS_CHANNEL_ID)
        if reports_channel:
            embed = create_report_embed(
                reporter=ctx.author,
                reported=member,
                reason=reason,
                channel=ctx.channel
            )
            await reports_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reports(bot))
