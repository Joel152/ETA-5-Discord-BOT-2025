import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from config import (
    DEPLOYMENT_CHANNEL_ID,
    DEPLOYMENT_PING_ROLE,
    AWAITING_TRYOUT_ID,
    MAIN_FACTION_ID,
)

class PollAndEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_poll_embed(self, poll_type: str, author: discord.Member, **kwargs) -> discord.Embed:
        """Creates a poll embed based on the type of poll."""
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")
        embed = discord.Embed(
            title=f"{poll_type} Poll",
            description=kwargs.get("description", "Vote below."),
            color=discord.Color.blue()
        )
        embed.add_field(name="Host", value=author.mention, inline=True)
        if kwargs.get("co_host"):
            embed.add_field(name="Co-Host", value=kwargs["co_host"].mention, inline=True)
        if kwargs.get("site"):
            embed.add_field(name="Site", value=kwargs["site"], inline=False)
        embed.set_footer(text=f"Time: {current_time} | Date: {current_date}")
        return embed

    def create_event_embed(self, event_type: str, author: discord.Member, **kwargs) -> discord.Embed:
        """Creates an event embed based on the type of event."""
        embed = self.create_poll_embed(event_type, author, **kwargs)
        embed.add_field(name="Instructions", value=kwargs.get("instructions", "Follow event-specific rules."), inline=False)
        embed.add_field(name="Course", value=kwargs.get("course", "Details to be added."), inline=False)
        return embed

    @commands.command(name="poll")
    async def poll_command(self, ctx, poll_type: str, *, additional_info=None):
        """Create a poll via prefix command."""
        poll_type = poll_type.lower()
        if poll_type not in ["deployment", "tryout", "training", "gamenight"]:
            await ctx.send("❌ Invalid poll type! Valid types: Deployment, Tryout, Training, Gamenight.")
            return

        channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not channel:
            await ctx.send("❌ Deployment channel not found. Please contact an administrator.")
            return

        if poll_type == "deployment":
            embed = self.create_poll_embed("Deployment", ctx.author, description="Deployment Poll")
            content = f"<@&{DEPLOYMENT_PING_ROLE}> Deployment?"
        elif poll_type == "tryout":
            embed = self.create_poll_embed(
                "Tryout",
                ctx.author,
                co_host=None,  # Replace with co-host if provided
                site="Site-45",
                description="Tryout Poll",
            )
            content = f"<@&{AWAITING_TRYOUT_ID}> Tryout?"
        else:
            embed = discord.Embed(
                title="Coming Soon",
                description=f"{poll_type.capitalize()} feature is under construction.",
                color=discord.Color.red(),
            )
            content = None

        poll_message = await channel.send(content=content, embed=embed)
        await poll_message.add_reaction("✅")
        await ctx.send(f"{poll_type.capitalize()} poll created in {channel.mention}.")

    @app_commands.command(name="poll", description="Create a poll")
    async def poll_slash(self, interaction: discord.Interaction, poll_type: str):
        """Create a poll via slash command."""
        await self.poll_command(interaction.channel, poll_type)

    @commands.command(name="event")
    async def event_command(self, ctx, event_type: str, *, additional_info=None):
        """Create an event via prefix command."""
        event_type = event_type.lower()
        if event_type not in ["deployment", "tryout", "training", "gamenight"]:
            await ctx.send("❌ Invalid event type! Valid types: Deployment, Tryout, Training, Gamenight.")
            return

        channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not channel:
            await ctx.send("❌ Event channel not found. Please contact an administrator.")
            return

        embed = self.create_event_embed(event_type.capitalize(), ctx.author, course=additional_info)
        content = f"<@&{MAIN_FACTION_ID}> {event_type.capitalize()} Event?"

        event_message = await channel.send(content=content, embed=embed)
        await event_message.add_reaction("✅")
        await ctx.send(f"{event_type.capitalize()} event created in {channel.mention}.")

    @app_commands.command(name="event", description="Create an event")
    async def event_slash(self, interaction: discord.Interaction, event_type: str):
        """Create an event via slash command."""
        await self.event_command(interaction.channel, event_type)

async def setup(bot):
    await bot.add_cog(PollAndEvent(bot))
