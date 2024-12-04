"""
Handles member join/leave events and welcome messages
"""
import discord
from discord.ext import commands
from config import WELCOME_CHANNEL_ID, FAREWELL_CHANNEL_ID
from .utils.embeds import create_welcome_embed, create_farewell_embed

class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when a member joins"""
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = create_welcome_embed(member)
            await channel.send(content=member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Send farewell message when a member leaves"""
        channel = member.guild.get_channel(FAREWELL_CHANNEL_ID)
        if channel:
            embed = create_farewell_embed(member)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))
