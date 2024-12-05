import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class UtilityCommands(commands.GroupCog, group_name="util"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="serverinfo", description="Display information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"{guild.name} Server Information",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Display information about a user")
    @app_commands.describe(member="The member to get information about")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        
        embed = discord.Embed(
            title=f"User Information - {member.name}",
            color=member.color
        )
        
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))
