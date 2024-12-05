import discord
from discord.ext import commands
from discord import app_commands, ui
from datetime import datetime
from config import (
    DEPLOYMENT_CHANNEL_ID,
    DEPLOYMENT_PING_ROLE,
    AWAITING_TRYOUT_ID,
    MAIN_FACTION_ID,
)

class EventDropdown(ui.Select):
    def __init__(self, bot, user, event_type):
        self.bot = bot
        self.user = user
        self.event_type = event_type

        options = [
            discord.SelectOption(label="Deployment", description="Create a Deployment event"),
            discord.SelectOption(label="Tryout", description="Create a Tryout event"),
            discord.SelectOption(label="Training", description="Create a Training event"),
            discord.SelectOption(label="Gamenight", description="Create a Gamenight event"),
        ]

        super().__init__(
            placeholder="Choose the type of event...",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        selected_type = self.values[0]

        # Send a follow-up prompt for more details based on event type
        if selected_type == "Deployment":
            embed = self.create_deployment_embed(self.user)
        elif selected_type == "Tryout":
            embed = self.create_tryout_embed(self.user)
        elif selected_type == "Training":
            embed = self.create_training_embed(self.user)
        elif selected_type == "Gamenight":
            embed = self.create_gamenight_embed(self.user)

        deployment_channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if deployment_channel:
            await deployment_channel.send(embed=embed)
            await interaction.response.send_message(f"{selected_type} event created in {deployment_channel.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message("Error: Deployment channel not found. Please contact an administrator.", ephemeral=True)

    def create_deployment_embed(self, author):
        embed = discord.Embed(
            title="Deployment Event",
            description="Vote below for the Deployment Event.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Host", value=author.mention, inline=False)
        embed.add_field(name="Site", value="Site-45", inline=False)
        embed.add_field(name="Reactions Needed", value="3+ reactions", inline=False)
        embed.set_footer(text=f"Created at {datetime.now().strftime('%H:%M')} | {datetime.now().strftime('%Y-%m-%d')}")
        return embed

    def create_tryout_embed(self, author):
        embed = discord.Embed(
            title="Tryout Event",
            description="Tryout for new team members.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Host", value=author.mention, inline=False)
        embed.add_field(name="Co-Host", value="TBA", inline=False)
        embed.add_field(name="Site", value="Site-45", inline=False)
        embed.add_field(name="Instructions", value="Spawn as [Team]. Say `!eta-5` on the radio.", inline=False)
        embed.set_footer(text=f"Created at {datetime.now().strftime('%H:%M')} | {datetime.now().strftime('%Y-%m-%d')}")
        return embed

    def create_training_embed(self, author):
        embed = discord.Embed(
            title="Training Event",
            description="Choose one of the training types.",
            color=discord.Color.green()
        )
        embed.add_field(name="Host", value=author.mention, inline=False)
        embed.add_field(name="Co-Host", value="N/A", inline=False)
        embed.add_field(name="Server Name", value="ETA-5 Training", inline=False)
        embed.add_field(name="Instructions", value="Join as MTF, STS upon spawn, and wait for further instructions.", inline=False)
        embed.set_footer(text=f"Created at {datetime.now().strftime('%H:%M')} | {datetime.now().strftime('%Y-%m-%d')}")
        return embed

    def create_gamenight_embed(self, author):
        embed = discord.Embed(
            title="Gamenight Event",
            description="A casual and fun gaming session for everyone!",
            color=discord.Color.purple()
        )
        embed.add_field(name="Host", value=author.mention, inline=False)
        embed.add_field(name="Details", value="Games and activities will be announced in the channel.", inline=False)
        embed.set_footer(text=f"Created at {datetime.now().strftime('%H:%M')} | {datetime.now().strftime('%Y-%m-%d')}")
        return embed


class EventDropdownView(ui.View):
    def __init__(self, bot, user):
        super().__init__(timeout=60)
        self.add_item(EventDropdown(bot, user, event_type=None))


class PollAndEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="event")
    async def event_command(self, ctx):
        """Create an event using a dropdown."""
        view = EventDropdownView(self.bot, ctx.author)
        await ctx.send("Please select the type of event from the dropdown below:", view=view)

    @app_commands.command(name="event", description="Create an event")
    async def event_slash(self, interaction: discord.Interaction):
        """Create an event using a slash command and dropdown."""
        view = EventDropdownView(self.bot, interaction.user)
        await interaction.response.send_message("Please select the type of event from the dropdown below:", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(PollAndEvent(bot))
