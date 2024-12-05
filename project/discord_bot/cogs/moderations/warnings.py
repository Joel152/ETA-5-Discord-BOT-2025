"""
Handles the warning system with both traditional and slash commands
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from config import MOD_ROLE_ID
from utils.logging import log_warning

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # Store warnings in memory: {user_id: [{moderator_id, reason, timestamp}]}

    def has_mod_role():
        def predicate(interaction: discord.Interaction) -> bool:
            return any(role.id == MOD_ROLE_ID for role in interaction.user.roles)
        return app_commands.check(predicate)

    async def cog_check(self, ctx):
        """Check if user has moderator role"""
        return any(role.id == MOD_ROLE_ID for role in ctx.author.roles)

    # Traditional Commands
    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason: str = None):
        """Warn a member"""
        if not reason:
            await ctx.send("❌ You must provide a reason for warning the member!")
            return

        try:
            if member.id not in self.warnings:
                self.warnings[member.id] = []
            
            self.warnings[member.id].append({
                'moderator_id': ctx.author.id,
                'reason': reason,
                'timestamp': datetime.utcnow()
            })
            
            warning_count = len(self.warnings[member.id])
            await log_warning(ctx.guild, member, ctx.author, reason)
            
            if warning_count >= 3:
                until = discord.utils.utcnow() + timedelta(days=1)
                await member.timeout(until=until, reason="Automatic timeout: 3 warnings received")
                await ctx.send(f"⚠️ {member.mention} has received 3 warnings and has been automatically timed out for 24 hours.")
            else:
                await ctx.send(f"✅ Warned {member.mention} | Warning {warning_count}/3 | Reason: {reason}")
                
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        """View warnings for a member"""
        if member.id not in self.warnings or not self.warnings[member.id]:
            await ctx.send(f"✅ {member.mention} has no warnings.")
            return

        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.orange()
        )
        
        for i, warning in enumerate(self.warnings[member.id], 1):
            moderator = ctx.guild.get_member(warning['moderator_id'])
            mod_name = moderator.name if moderator else "Unknown Moderator"
            
            embed.add_field(
                name=f"Warning {i}",
                value=f"**Reason:** {warning['reason']}\n**By:** {mod_name}\n**Date:** {warning['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}",
                inline=False
            )

        await ctx.send(embed=embed)

    # Slash Commands
    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.describe(
        member="The member to warn",
        reason="The reason for the warning"
    )
    @has_mod_role()
    async def slash_warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            if member.id not in self.warnings:
                self.warnings[member.id] = []
            
            self.warnings[member.id].append({
                'moderator_id': interaction.user.id,
                'reason': reason,
                'timestamp': datetime.utcnow()
            })
            
            warning_count = len(self.warnings[member.id])
            await log_warning(interaction.guild, member, interaction.user, reason)
            
            if warning_count >= 3:
                until = discord.utils.utcnow() + timedelta(days=1)
                await member.timeout(until=until, reason="Automatic timeout: 3 warnings received")
                await interaction.response.send_message(
                    f"⚠️ {member.mention} has received 3 warnings and has been automatically timed out for 24 hours."
                )
            else:
                await interaction.response.send_message(
                    f"✅ Warned {member.mention} | Warning {warning_count}/3 | Reason: {reason}"
                )
                
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="warnings", description="View warnings for a member")
    @app_commands.describe(member="The member to check warnings for")
    @has_mod_role()
    async def slash_warnings(self, interaction: discord.Interaction, member: discord.Member):
        if member.id not in self.warnings or not self.warnings[member.id]:
            await interaction.response.send_message(f"✅ {member.mention} has no warnings.")
            return

        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.orange()
        )
        
        for i, warning in enumerate(self.warnings[member.id], 1):
            moderator = interaction.guild.get_member(warning['moderator_id'])
            mod_name = moderator.name if moderator else "Unknown Moderator"
            
            embed.add_field(
                name=f"Warning {i}",
                value=f"**Reason:** {warning['reason']}\n**By:** {mod_name}\n**Date:** {warning['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Warnings(bot))
