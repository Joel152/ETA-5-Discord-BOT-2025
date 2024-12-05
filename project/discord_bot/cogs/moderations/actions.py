"""
Handles moderation actions like kick, ban, timeout with both traditional and slash commands
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from config import MOD_ROLE_ID
from ...utils.logging import log_kick, log_ban, log_timeout

class ModerationActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_mod_role():
        def predicate(interaction: discord.Interaction) -> bool:
            return any(role.id == MOD_ROLE_ID for role in interaction.user.roles)
        return app_commands.check(predicate)

    async def cog_check(self, ctx):
        """Check if user has moderator role for traditional commands"""
        return any(role.id == MOD_ROLE_ID for role in ctx.author.roles)

    # Traditional Commands
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

    # Slash Commands
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(
        member="The member to kick",
        reason="The reason for kicking the member"
    )
    @has_mod_role()
    async def slash_kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await member.kick(reason=reason)
            await log_kick(interaction.guild, member, interaction.user, reason)
            await interaction.response.send_message(f"✅ Kicked {member.mention} | Reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to kick that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(
        member="The member to ban",
        reason="The reason for banning the member",
        delete_days="Number of days of messages to delete"
    )
    @has_mod_role()
    async def slash_ban(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        reason: str,
        delete_days: app_commands.Range[int, 0, 7] = 1
    ):
        try:
            await member.ban(reason=reason, delete_message_days=delete_days)
            await log_ban(interaction.guild, member, interaction.user, reason)
            await interaction.response.send_message(f"✅ Banned {member.mention} | Reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to ban that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.describe(
        member="The member to timeout",
        duration="Duration in minutes",
        reason="The reason for the timeout"
    )
    @has_mod_role()
    async def slash_timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: app_commands.Range[int, 1, 40320],  # Max 28 days
        reason: str
    ):
        try:
            until = discord.utils.utcnow() + timedelta(minutes=duration)
            await member.timeout(until=until, reason=reason)
            await log_timeout(interaction.guild, member, interaction.user, duration, reason)
            await interaction.response.send_message(
                f"✅ Timed out {member.mention} for {duration} minutes | Reason: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to timeout that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationActions(bot))
