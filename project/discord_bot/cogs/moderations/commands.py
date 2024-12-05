import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from ...config import MOD_ROLE_ID
from ...utils.logging import log_kick, log_ban, log_timeout, log_warning
from ...utils.embeds import create_mod_action_embed

class ModerationCommands(commands.GroupCog, group_name="mod"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    def has_mod_role():
        def predicate(interaction: discord.Interaction) -> bool:
            return any(role.id == MOD_ROLE_ID for role in interaction.user.roles)
        return app_commands.check(predicate)

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(
        member="The member to kick",
        reason="The reason for kicking the member"
    )
    @has_mod_role()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await member.kick(reason=reason)
            await log_kick(interaction.guild, member, interaction.user, reason)
            
            embed = create_mod_action_embed("Kick", interaction.user, member, reason)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to kick that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(
        member="The member to ban",
        reason="The reason for banning the member",
        delete_days="Number of days of messages to delete"
    )
    @has_mod_role()
    async def ban(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        reason: str,
        delete_days: app_commands.Range[int, 0, 7] = 1
    ):
        try:
            await member.ban(reason=reason, delete_message_days=delete_days)
            await log_ban(interaction.guild, member, interaction.user, reason)
            
            embed = create_mod_action_embed("Ban", interaction.user, member, reason)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to ban that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.describe(
        member="The member to timeout",
        duration="Duration in minutes",
        reason="The reason for the timeout"
    )
    @has_mod_role()
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: app_commands.Range[int, 1, 40320],  # Max 28 days
        reason: str
    ):
        try:
            until = discord.utils.utcnow() + timedelta(minutes=duration)
            await member.timeout(until=until, reason=reason)
            await log_timeout(interaction.guild, member, interaction.user, duration, reason)
            
            embed = create_mod_action_embed("Timeout", interaction.user, member, f"{reason} (Duration: {duration} minutes)")
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to timeout that member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.describe(
        member="The member to warn",
        reason="The reason for the warning"
    )
    @has_mod_role()
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await log_warning(interaction.guild, member, interaction.user, reason)
            
            embed = create_mod_action_embed("Warning", interaction.user, member, reason)
            await interaction.response.send_message(embed=embed)
            
            # DM the warned user
            try:
                warn_dm = discord.Embed(
                    title="Warning Received",
                    description=f"You have been warned in {interaction.guild.name}",
                    color=discord.Color.yellow()
                )
                warn_dm.add_field(name="Reason", value=reason)
                await member.send(embed=warn_dm)
            except discord.Forbidden:
                await interaction.followup.send("Note: Could not DM the user about their warning.", ephemeral=True)
                
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
