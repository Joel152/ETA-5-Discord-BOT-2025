import discord
from discord import app_commands
from discord.ext import commands
from ...config import OFFICER_ROLE_ID, SUPPORT_CHANNEL_ID, MOD_ROLE_ID

class SupportCommands(commands.GroupCog, group_name="support"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="officer", description="Request help from an officer")
    async def officer(self, interaction: discord.Interaction):
        support_channel = interaction.guild.get_channel(SUPPORT_CHANNEL_ID)
        if not support_channel:
            await interaction.response.send_message("Error: Support channel not configured.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Officer Help Request",
            description=f"{interaction.user.mention} needs help!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Channel", value=interaction.channel.mention)
        
        await support_channel.send(
            content=f"<@&{OFFICER_ROLE_ID}>",
            embed=embed
        )
        
        await interaction.response.send_message("✅ Officers have been notified!", ephemeral=True)

    @app_commands.command(name="dmt", description="Request help from Discord Moderators")
    @app_commands.describe(
        report_type="Type of report",
        message_link="Optional message link for reference"
    )
    @app_commands.choices(report_type=[
        app_commands.Choice(name="Spam", value="spam"),
        app_commands.Choice(name="Harassment", value="harassment"),
        app_commands.Choice(name="NSFW Content", value="nsfw"),
        app_commands.Choice(name="Other", value="other")
    ])
    async def dmt(
        self,
        interaction: discord.Interaction,
        report_type: app_commands.Choice[str],
        message_link: str = None
    ):
        support_channel = interaction.guild.get_channel(SUPPORT_CHANNEL_ID)
        if not support_channel:
            await interaction.response.send_message("Error: Support channel not configured.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Moderator Help Request",
            description=f"{interaction.user.mention} needs moderator assistance!",
            color=discord.Color.red()
        )
        embed.add_field(name="Report Type", value=report_type.name, inline=True)
        embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
        
        if message_link:
            embed.add_field(name="Message Reference", value=message_link, inline=False)

        await support_channel.send(
            content=f"<@&{MOD_ROLE_ID}>",
            embed=embed
        )
        
        await interaction.response.send_message("✅ Moderators have been notified!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SupportCommands(bot))
