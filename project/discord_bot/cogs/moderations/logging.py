"""
Utility functions for logging moderation actions in a thread
"""
import discord
from datetime import datetime
from config import MODERATION_CHANNEL_ID, MODERATION_THREAD_ID

async def get_log_thread(guild: discord.Guild) -> discord.Thread:
    """Get or notify about the logging thread"""
    channel = guild.get_channel(MODERATION_CHANNEL_ID)
    if not channel:
        return None

    thread = channel.get_thread(MODERATION_THREAD_ID)
    if not thread:
        # Notify moderators that the thread is missing
        await channel.send(f"⚠️ Warning: Moderation log thread not found! Please check the thread ID: {MODERATION_THREAD_ID}")
        return None
        
    return thread

async def log_warning(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a warning action"""
    thread = await get_log_thread(guild)
    if thread:
        await thread.send(
            f"⚠️ **Warning**\n"
            f"User {target.mention} (`{target.id}`) has been warned by {moderator.mention}\n"
            f"**Reason:** {reason}"
        )

async def log_kick(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a kick action"""
    thread = await get_log_thread(guild)
    if thread:
        await thread.send(
            f"👢 **Kick**\n"
            f"User {target.mention} (`{target.id}`) has been kicked by {moderator.mention}\n"
            f"**Reason:** {reason}"
        )

async def log_ban(guild: discord.Guild, target: discord.Member, moderator: discord.Member, reason: str):
    """Log a ban action"""
    thread = await get_log_thread(guild)
    if thread:
        await thread.send(
            f"🔨 **Ban**\n"
            f"User {target.mention} (`{target.id}`) has been banned by {moderator.mention}\n"
            f"**Reason:** {reason}"
        )

async def log_timeout(guild: discord.Guild, target: discord.Member, moderator: discord.Member, duration: int, reason: str):
    """Log a timeout action"""
    thread = await get_log_thread(guild)
    if thread:
        await thread.send(
            f"⏰ **Timeout**\n"
            f"User {target.mention} (`{target.id}`) has been put in timeout by {moderator.mention}\n"
            f"**Duration:** {duration} minutes\n"
            f"**Reason:** {reason}"
        )
