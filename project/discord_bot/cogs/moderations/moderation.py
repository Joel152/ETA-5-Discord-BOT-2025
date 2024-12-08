import discord
from discord import app_commands
from discord.ext import commands
from config import (
    OFFICER_ROLE_ID,
    SUPPORT_CHANNEL_ID,
    MOD_ROLE_ID,
    MOD_SUPPORT_CHANNEL_ID
)
from utils.report_templates import REPORT_TEMPLATES

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['mod'])
    async def officer(self, ctx):
        """
        Ping officers for help in the support channel
        Usage: !officer or !mod
        """
        support_channel = self.bot.get_channel(SUPPORT_CHANNEL_ID)
        if not support_channel:
            await ctx.send("Error: Support channel not found. Please contact an administrator.")
            return

        officer_role = ctx.guild.get_role(OFFICER_ROLE_ID)
        if not officer_role:
            await ctx.send("Error: Officer role not found. Please contact an administrator.")
            return

        message = (
            f"{ctx.author.mention} needs help in {ctx.channel.mention}\n"
            f"{officer_role.mention}"
        )

        await support_channel.send(message)
        await ctx.send(f"Officers have been notified and will assist you soon!")

    @commands.command()
    async def dmt(self, ctx, report_type: str = "other", message_link: str = None):
        """
        Ping moderators for help
        Usage: !dmt [report_type] [message_link]
        """
        mod_channel = self.bot.get_channel(MOD_SUPPORT_CHANNEL_ID)
        if not mod_channel:
            await ctx.send("Error: Mod channel not found. Please contact an administrator.")
            return

        mod_role = ctx.guild.get_role(MOD_ROLE_ID)
        if not mod_role:
            await ctx.send("Error: Mod role not found. Please contact an administrator.")
            return

        report_template = REPORT_TEMPLATES.get(report_type.lower(), REPORT_TEMPLATES["other"])
        
        embed = discord.Embed(
            title=report_template["title"],
            description=report_template["description"],
            color=report_template["color"]
        )
        embed.add_field(name="Reporter", value=ctx.author.mention, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        if message_link:
            embed.add_field(name="Message Link", value=message_link, inline=False)

        await mod_channel.send(content=f"{mod_role.mention}", embed=embed)
        await ctx.send("Moderators have been notified and will review your report soon.")

    @app_commands.command(name="dmt", description="Request moderator assistance with a pre-made report")
    @app_commands.choices(report_type=[
        app_commands.Choice(name="Spam", value="spam"),
        app_commands.Choice(name="Harassment", value="harassment"),
        app_commands.Choice(name="NSFW Content", value="nsfw"),
        app_commands.Choice(name="Raid Alert", value="raid"),
        app_commands.Choice(name="Other", value="other"),
    ])
    async def dmt_slash(
        self,
        interaction: discord.Interaction,
        report_type: str,
        message_link: str = None
    ):
        """Slash command version of the dmt command"""
        mod_channel = self.bot.get_channel(MOD_SUPPORT_CHANNEL_ID)
        if not mod_channel:
            await interaction.response.send_message(
                "Error: Mod channel not found. Please contact an administrator.",
                ephemeral=True
            )
            return

        mod_role = interaction.guild.get_role(MOD_ROLE_ID)
        if not mod_role:
            await interaction.response.send_message(
                "Error: Mod role not found. Please contact an administrator.",
                ephemeral=True
            )
            return

        report_template = REPORT_TEMPLATES.get(report_type.lower(), REPORT_TEMPLATES["other"])
        
        embed = discord.Embed(
            title=report_template["title"],
            description=report_template["description"],
            color=report_template["color"]
        )
        embed.add_field(name="Reporter", value=interaction.user.mention, inline=True)
        embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
        if message_link:
            embed.add_field(name="Message Link", value=message_link, inline=False)

        await mod_channel.send(content=f"{mod_role.mention}", embed=embed)
        await interaction.response.send_message(
            "Moderators have been notified and will review your report soon.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
