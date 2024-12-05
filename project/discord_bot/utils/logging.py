"""
Comprehensive logging system for moderation actions
"""
import discord
from datetime import datetime
from config import MODERATION_CHANNEL_ID, MODERATION_THREAD_ID  # Fetch IDs from the configuration file

class ModLogger:
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self._log_channel = None
        self._log_thread = None

    async def get_log_channel(self) -> discord.TextChannel:
        """Get the logging channel"""
        if not self._log_channel:
            self._log_channel = self.guild.get_channel(MODERATION_CHANNEL_ID)
        return self._log_channel

    async def get_log_thread(self) -> discord.Thread:
        """Get the logging thread"""
        if not self._log_thread:
            channel = await self.get_log_channel()
            if channel:
                self._log_thread = discord.utils.get(channel.threads, id=MODERATION_THREAD_ID)
        return self._log_thread

    async def create_log_embed(
        self,
        action: str,
        target: discord.Member,
        moderator: discord.Member,
        reason: str,
        **kwargs
    ) -> discord.Embed:
        """Create a standardized embed for logging"""
        color_map = {
            "Kick": discord.Color.orange(),
            "Ban": discord.Color.red(),
            "Timeout": discord.Color.yellow(),
            "Warning": discord.Color.gold(),
            "Unban": discord.Color.green(),
            "Report": discord.Color.blue()
        }

        embed = discord.Embed(
            title=f"Moderation Action: {action}",
            color=color_map.get(action, discord.Color.greyple()),
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="Target", value=f"{target.mention} (`{target.id}`)", inline=True)
        embed.add_field(name="Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)

        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            embed.add_field(name=key.replace('_', ' ').title(), value=str(value), inline=True)

        embed.set_footer(text=f"User ID: {target.id}")
        
        if target.display_avatar:
            embed.set_thumbnail(url=target.display_avatar.url)

        return embed

    async def log_action(
        self,
        action: str,
        target: discord.Member,
        moderator: discord.Member,
        reason: str,
        **kwargs
    ) -> bool:
        """Log a moderation action to the designated channel or thread"""
        try:
            thread = await self.get_log_thread()
            embed = await self.create_log_embed(action, target, moderator, reason, **kwargs)
            
            if thread:
                await thread.send(embed=embed)
            else:
                channel = await self.get_log_channel()
                if not channel:
                    return False
                await channel.send(embed=embed)
            return True
        except Exception as e:
            print(f"Error logging moderation action: {e}")
            return False


# Helper functions for specific moderation actions
async def log_kick(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a kick action"""
    logger = ModLogger(guild)
    await logger.log_action("Kick", target, moderator, reason)

async def log_ban(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a ban action"""
    logger = ModLogger(guild)
    await logger.log_action("Ban", target, moderator, reason)

async def log_timeout(guild: discord.Guild, target: discord.Member, moderator: discord.Member, duration: int, reason: str):
    """Log a timeout action"""
    logger = ModLogger(guild)
    await logger.log_action("Timeout", target, moderator, reason, duration=f"{duration} minutes")

async def log_warning(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a warning action"""
    logger = ModLogger(guild)
    await logger.log_action("Warning", target, moderator, reason)

async def log_unban(guild: discord.Guild, target: discord.User, moderator: discord.Member, reason: str):
    """Log an unban action"""
    logger = ModLogger(guild)
    await logger.log_action("Unban", target, moderator, reason)

async def log_report(
    guild: discord.Guild,
    target: discord.Member,
    reporter: discord.Member,
    reason: str,
    channel: discord.TextChannel,
    evidence: str = None
):
    """Log a user report"""
    logger = ModLogger(guild)
    kwargs = {"Channel": channel.mention}
    if evidence:
        kwargs["Evidence"] = evidence
    await logger.log_action("Report", target, reporter, reason, **kwargs)
