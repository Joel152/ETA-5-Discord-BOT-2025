"""
Utility functions for creating embedded messages
"""
import discord
from datetime import datetime

def create_mod_action_embed(action: str, moderator: discord.Member, target: discord.Member, reason: str) -> discord.Embed:
    """Create an embed for moderator actions"""
    embed = discord.Embed(
        title=f"Moderation Action: {action}",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Target", value=f"{target.mention} ({target.id})", inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    return embed

def create_welcome_embed(member: discord.Member) -> discord.Embed:
    """Create a welcome message embed"""
    embed = discord.Embed(
        title="Welcome to the Server! :tada:",
        description=f"Welcome {member.mention} to {member.guild.name}!",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(
        name="Getting Started",
        value="• Please read the rules in #rules\n• Introduce yourself in #introductions\n• Get roles in #role-assignment",
        inline=False
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    return embed

def create_farewell_embed(member: discord.Member) -> discord.Embed:
    """Create a farewell message embed"""
    embed = discord.Embed(
        title="Member Left",
        description=f"**{member}** has left the server",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    return embed

def create_report_embed(reporter: discord.Member, reported: discord.Member, reason: str, channel: discord.TextChannel) -> discord.Embed:
    """Create an embed for user reports"""
    embed = discord.Embed(
        title="New User Report",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Reported User", value=f"{reported.mention} ({reported.id})", inline=True)
    embed.add_field(name="Reported By", value=f"{reporter.mention} ({reporter.id})", inline=True)
    embed.add_field(name="Channel", value=channel.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    return embed
