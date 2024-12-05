"""
Handles user reports and incident management with both traditional and slash commands
"""
import discord
from discord import app_commands
from discord.ext import commands
from ..config import REPORTS_CHANNEL_ID, MOD_ROLE_ID
from ..utils.embeds import create_report_embed

class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Traditional Command
    @commands.command()
    async def report(self, ctx, member: discord.Member, *, reason: str):
        """Report a user for breaking rules"""
        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await ctx.author.send("✅ Your report has been submitted to the moderators. Thank you for helping keep the server safe!")
        except discord.Forbidden:
            pass

        reports_channel = ctx.guild.get_channel(REPORTS_CHANNEL_ID)
        if reports_channel:
            embed = create_report_embed(
                reporter=ctx.author,
                reported=member,
                reason=reason,
                channel=ctx.channel
            )
            await reports_channel.send(content=f"<@&{MOD_ROLE_ID}>", embed=embed)

    # Slash Command
    @app_commands.command(name="report", description="Report a user for breaking rules")
    @app_commands.describe(
        member="The member to report",
        reason="The reason for reporting",
        evidence="Optional link to evidence (message link, screenshot, etc.)"
    )
    async def slash_report(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
        evidence: str = None
    ):
        try:
            await interaction.user.send(
                "✅ Your report has been submitted to the moderators. Thank you for helping keep the server safe!"
            )
        except discord.Forbidden:
            pass

        reports_channel = interaction.guild.get_channel(REPORTS_CHANNEL_ID)
        if reports_channel:
            embed = discord.Embed(
                title="User Report",
                description=f"Report against {member.mention}",
                color=discord.Color.red()
            )
            embed.add_field(name="Reporter", value=interaction.user.mention, inline=True)
            embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            
            if evidence:
                embed.add_field(name="Evidence", value=evidence, inline=False)
                
            embed.set_footer(text=f"User ID: {member.id}")
            embed.timestamp = discord.utils.utcnow()

            await reports_channel.send(content=f"<@&{MOD_ROLE_ID}>", embed=embed)
            
        await interaction.response.send_message("✅ Your report has been submitted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Reports(bot))
