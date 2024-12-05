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

    def generate_embed(self, title: str, description: str, author: discord.Member, **kwargs) -> discord.Embed:
        """
        Generate a customizable embed with dynamic fields.
        """
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
        
        if "host" in kwargs:
            embed.add_field(name="Host", value=kwargs["host"].mention, inline=True)
        if "co_host" in kwargs and kwargs["co_host"]:
            embed.add_field(name="Co-Host", value=kwargs["co_host"].mention, inline=True)
        if "site" in kwargs:
            embed.add_field(name="Site", value=kwargs["site"], inline=False)
        if "spawn" in kwargs:
            embed.add_field(name="Spawn", value=kwargs["spawn"], inline=False)
        if "instructions" in kwargs:
            embed.add_field(name="Instructions", value=kwargs["instructions"], inline=False)
        if "course" in kwargs:
            embed.add_field(name="Course", value=kwargs["course"], inline=False)
        
        embed.set_footer(text=f"Time: {current_time} | Date: {current_date}")
        return embed

    async def post_poll_or_event(
        self,
        interaction_or_context,
        event_type: str,
        host: discord.Member,
        co_host: discord.Member = None,
        site: str = None,
        spawn: str = None,
        instructions: str = None,
        course: str = None,
    ):
        """
        Handles the posting of polls or events to the appropriate channel.
        """
        channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not channel:
            await interaction_or_context.send("❌ Deployment channel not found. Please contact an administrator.")
            return
        
        embed = self.generate_embed(
            title=f"{event_type} Event",
            description=f"{event_type} poll or event created!",
            author=host,
            host=host,
            co_host=co_host,
            site=site,
            spawn=spawn,
            instructions=instructions,
            course=course,
        )
        
        content = None
        if event_type.lower() == "deployment":
            content = f"<@&{DEPLOYMENT_PING_ROLE}> Deployment?"
        elif event_type.lower() == "tryout":
            content = f"<@&{AWAITING_TRYOUT_ID}> Tryout?"
        elif event_type.lower() in ["training", "gamenight"]:
            content = f"<@&{MAIN_FACTION_ID}> {event_type.capitalize()} Event!"
        
        message = await channel.send(content=content, embed=embed)
        await message.add_reaction("✅")
        if isinstance(interaction_or_context, discord.Interaction):
            await interaction_or_context.response.send_message(f"{event_type.capitalize()} posted in {channel.mention}.")
        else:
            await interaction_or_context.send(f"{event_type.capitalize()} posted in {channel.mention}.")

    @commands.command(name="poll")
    async def poll_command(self, ctx, event_type: str):
        """
        Prefix command to create a poll for a specified event type.
        """
        if event_type.lower() not in ["deployment", "tryout", "training", "gamenight"]:
            await ctx.send("❌ Invalid event type! Valid types: Deployment, Tryout, Training, Gamenight.")
            return
        await self.post_poll_or_event(ctx, event_type.capitalize(), host=ctx.author)

    @app_commands.command(name="poll", description="Create a poll for an event.")
    @app_commands.choices(
        event_type=[
            app_commands.Choice(name="Deployment", value="deployment"),
            app_commands.Choice(name="Tryout", value="tryout"),
            app_commands.Choice(name="Training", value="training"),
            app_commands.Choice(name="Gamenight", value="gamenight"),
        ]
    )
    async def poll_slash(self, interaction: discord.Interaction, event_type: app_commands.Choice[str]):
        """
        Slash command to create a poll for a specified event type.
        """
        await self.post_poll_or_event(interaction, event_type.name.capitalize(), host=interaction.user)

    @commands.command(name="event")
    async def event_command(
        self,
        ctx,
        event_type: str,
        site: str = "Site-45",
        spawn: str = "Spawn as ETA-5",
        instructions: str = "Follow event rules.",
        course: str = "Details to be added.",
    ):
        """
        Prefix command to create an event with detailed configurations.
        """
        if event_type.lower() not in ["deployment", "tryout", "training", "gamenight"]:
            await ctx.send("❌ Invalid event type! Valid types: Deployment, Tryout, Training, Gamenight.")
            return
        await self.post_poll_or_event(
            ctx,
            event_type.capitalize(),
            host=ctx.author,
            site=site,
            spawn=spawn,
            instructions=instructions,
            course=course,
        )

    @app_commands.command(name="event", description="Create an event with details.")
    @app_commands.choices(
        event_type=[
            app_commands.Choice(name="Deployment", value="deployment"),
            app_commands.Choice(name="Tryout", value="tryout"),
            app_commands.Choice(name="Training", value="training"),
            app_commands.Choice(name="Gamenight", value="gamenight"),
        ]
    )
    async def event_slash(
        self,
        interaction: discord.Interaction,
        event_type: app_commands.Choice[str],
        site: str = "Site-45",
        spawn: str = "Spawn as ETA-5",
        instructions: str = "Follow event rules.",
        course: str = "Details to be added.",
    ):
        """
        Slash command to create an event with detailed configurations.
        """
        await self.post_poll_or_event(
            interaction,
            event_type.name.capitalize(),
            host=interaction.user,
            site=site,
            spawn=spawn,
            instructions=instructions,
            course=course,
        )


async def setup(bot):
    await bot.add_cog(PollAndEvent(bot))
