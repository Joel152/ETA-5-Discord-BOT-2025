"""
Handles the warning system
"""
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from config import MOD_ROLE_ID
from utils.logging import log_warning

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # Store warnings in memory: {user_id: [{moderator_id, reason, timestamp}]}

    async def cog_check(self, ctx):
        """Check if user has moderator role"""
        return any(role.id == MOD_ROLE_ID for role in ctx.author.roles)

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason: str = None):
        """Warn a member"""
        if not reason:
            await ctx.send("❌ You must provide a reason for warning the member!")
            return

        try:
            # Add warning to memory
            if member.id not in self.warnings:
                self.warnings[member.id] = []
            
            self.warnings[member.id].append({
                'moderator_id': ctx.author.id,
                'reason': reason,
                'timestamp': datetime.utcnow()
            })
            
            warning_count = len(self.warnings[member.id])
            
            # Log the warning
            await log_warning(ctx.guild, member, ctx.author, reason)
            
            # Check for automatic punishments
            if warning_count >= 3:
                # Timeout for 24 hours after 3 warnings
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

async def setup(bot):
    await bot.add_cog(Warnings(bot))