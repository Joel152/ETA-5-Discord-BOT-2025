import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional
from config import (
    DEPLOYMENT_CHANNEL_ID,
    DEPLOYMENT_PING_ROLE,
    AWAITING_TRYOUT_ID,
    MAIN_FACTION_ID,
)


class PollAndEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, event_type: str, author: discord.Member, **kwargs) -> discord.Embed:
        """
        Creates a preset embed for the selected event type with user-provided inputs.
        """
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")

        embed = discord.Embed(
            title=f"{event_type} Event",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Host", value=author.mention, inline=True)
        
        if kwargs.get("co_host"):
            embed.add_field(name="Co-Host", value=kwargs["co_host"].mention, inline=True)
        
        if kwargs.get("site"):
            embed.add_field(name="Site", value=kwargs["site"], inline=True)
        
        if kwargs.get("spawn"):
            embed.add_field(name="Spawn", value=kwargs["spawn"], inline=False)
        
        embed.add_field(name="Details", value=kwargs.get("details", "Follow event-specific instructions."), inline=False)
        embed.set_footer(text=f"Time: {current_time} | Date: {current_date}")

        return embed

    @commands.command(name="poll")
    async def poll_command(self, ctx, event_type: str, site: Optional[str] = None, spawn: Optional[str] = None):
        """
        Create a poll via prefix command.
        """
        event_type = event_type.capitalize()
        valid_types = ["Deployment", "Tryout", "Training", "Gamenight"]

        if event_type not in valid_types:
            await ctx.send(f"❌ Invalid event type! Valid types: {', '.join(valid_types)}.")
            return

        channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not channel:
            await ctx.send("❌ Deployment channel not found. Please contact an administrator.")
            return

        # Event-specific settings
        if event_type == "Deployment":
            content = f"<@&{DEPLOYMENT_PING_ROLE}> Deployment Poll!"
            details = "Vote below."
        elif event_type == "Tryout":
            content = f"<@&{AWAITING_TRYOUT_ID}> Tryout Poll!"
            details = (
                "**How to Join?**\n"
                "- Spawn as [Team]\n"
                "- Say `!eta-5` on the radio\n\n"
                "**Rules:**\n"
                "- Follow OOS (Oath of Silence).\n"
                "- Stay with the host as much as you can.\n"
                "- No trolling or goofing around.\n"
                "- Follow site rules at all times."
            )
        elif event_type == "Training":
            content = f"<@&{MAIN_FACTION_ID}> Training Poll!"
            details = "Training details vary. Check event-specific announcements."
        else:  # Gamenight
            content = "🎮 Gamenight! Join us for fun and games!"
            details = "Bring your friends and have a great time!"

        embed = self.create_embed(
            event_type, ctx.author, site=site, spawn=spawn, details=details
        )
        poll_message = await channel.send(content=content, embed=embed)
        await poll_message.add_reaction("✅")
        await ctx.send(f"{event_type} poll created in {channel.mention}.")

    @app_commands.command(name="poll", description="Create a poll for events like Deployment, Training, etc.")
    @app_commands.choices(
        event_type=[
            app_commands.Choice(name="Deployment", value="Deployment"),
            app_commands.Choice(name="Tryout", value="Tryout"),
            app_commands.Choice(name="Training", value="Training"),
            app_commands.Choice(name="Gamenight", value="Gamenight"),
        ]
    )
    async def poll_slash(
        self, interaction: discord.Interaction, event_type: app_commands.Choice[str], site: Optional[str] = None, spawn: Optional[str] = None
    ):
        """
        Slash command for creating a poll.
        """
        await self.poll_command(interaction, event_type.value, site=site, spawn=spawn)

    @commands.command(name="event")
    async def event_command(self, ctx, event_type: str, *, additional_info=None):
        """
        Create an event announcement via prefix command.
        """
        await self.poll_command(ctx, event_type, additional_info)

    @app_commands.command(name="event", description="Create an event announcement.")
    async def event_slash(self, interaction: discord.Interaction, event_type: str):
        """
        Slash command for creating an event announcement.
        """
        await self.event_command(interaction.channel, event_type)

async def setup(bot):
    await bot.add_cog(PollAndEvent(bot))
