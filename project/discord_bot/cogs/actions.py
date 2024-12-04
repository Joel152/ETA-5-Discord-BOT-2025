"""
Handles moderation actions like kick, ban, timeout
"""
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from config import MOD_ROLE_ID
from utils.logging import log_kick, log_ban, log_timeout

class ModerationActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Check if user has moderator role"""
        return any(role.id == MOD_ROLE_ID for role in ctx.author.roles)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kick a member from the server"""
        if not reason:
            await ctx.send("❌ You must provide a reason for kicking the member!")
            return

        try:
            await member.kick(reason=reason)
            await log_kick(ctx.guild, member, ctx.author, reason)
            await ctx.send(f"✅ Kicked {member.mention} | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick that member!")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Ban a member from the server"""
        if not reason:
            await ctx.send("❌ You must provide a reason for banning the member!")
            return

        try:
            await member.ban(reason=reason, delete_message_days=1)
            await log_ban(ctx.guild, member, ctx.author, reason)
            await ctx.send(f"✅ Banned {member.mention} | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban that member!")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command()
    async def timeout(self, ctx, member: discord.Member, duration: int, *, reason: str = None):
        """Timeout a member (duration in minutes)"""
        if not reason:
            await ctx.send("❌ You must provide a reason for timing out the member!")
            return

        try:
            until = datetime.utcnow() + timedelta(minutes=duration)
            await member.timeout(until=until, reason=reason)
            await log_timeout(ctx.guild, member, ctx.author, duration, reason)
            await ctx.send(f"✅ Timed out {member.mention} for {duration} minutes | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to timeout that member!")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(ModerationActions(bot))