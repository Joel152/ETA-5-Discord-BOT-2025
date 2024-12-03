import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import logging
from config import APPLICATIONS_CHANNEL_ID, GOOGLE_SPREADSHEET_ID, APP_READ_ID, RESULTS_CHANNEL_ID
from utils.google_forms import GoogleFormsAPI

logger = logging.getLogger('discord_bot')

class ApplicationView(discord.ui.View):
    def __init__(self, application_id: str):
        super().__init__(timeout=None)
        self.application_id = application_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_decision(interaction, "accepted")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_decision(interaction, "denied")

    async def process_decision(self, interaction: discord.Interaction, decision: str):
        # Check if the user has permission
        if not any(role.id == APP_READ_ID for role in interaction.user.roles):
            await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
            return

        # Fetch the results channel
        results_channel = interaction.guild.get_channel(RESULTS_CHANNEL_ID)
        if not results_channel:
            await interaction.response.send_message("Error: Results channel not found. Please contact an admin.", ephemeral=True)
            return

        # Create an embed for the result
        embed = discord.Embed(
            title=f"Application {decision.capitalize()}",
            description=f"Application ID: {self.application_id}",
            color=discord.Color.green() if decision == "accepted" else discord.Color.red()
        )
        embed.add_field(name="Decided by", value=interaction.user.mention)
        embed.add_field(name="Decision", value=decision.capitalize())
        embed.timestamp = datetime.now()

        # Send the result to the results channel
        await results_channel.send(embed=embed)
        # Update the original message
        await interaction.message.edit(view=None)
        # Notify the user
        await interaction.response.send_message(f"Application {decision}!", ephemeral=True)

def create_application_embed(application_id: int, response: list) -> discord.Embed:
    embed = discord.Embed(
        title=f"New Application #{application_id}",
        description="Application details below:",
        color=discord.Color.blue()
    )

    embed.add_field(name="Discord User", value=response[0], inline=True)
    embed.add_field(name="Discord ID", value=response[1], inline=True)
    embed.add_field(name="Roblox User", value=response[2], inline=False)
    embed.add_field(name="Qn. 1: First thing to get morphed?", value=response[3], inline=False)
    embed.add_field(name="Qn. 2: Basic Faces?", value=response[4], inline=False)
    embed.add_field(name="Qn. 3: Basic Formations?", value=response[5], inline=False)
    embed.add_field(name="Qn. 4: Activity Rating (1-5)", value=response[6], inline=True)
    embed.add_field(name="Qn. 5: Allowed to break OOS?", value=response[7], inline=False)
    embed.add_field(name="Qn. 6: Responding to unknown ETA-5 member?", value=response[8], inline=False)
    embed.add_field(name="Questions/Concerns", value=response[9] if response[9] else "N/A", inline=False)

    embed.timestamp = datetime.now()
    return embed

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_forms = GoogleFormsAPI('project/discord_bot/credentials.json')
        self.last_processed_row = 0
        self.check_applications.start()

    def cog_unload(self):
        self.check_applications.cancel()

    @tasks.loop(minutes=1)
    async def check_applications(self):
        try:
            await self.process_new_applications()
        except Exception as e:
            logger.error(f"Error checking applications: {e}")

    async def process_new_applications(self):
        try:
            # Authenticate Google Forms API
            if not self.google_forms.service:
                await self.google_forms.authenticate()

            # Fetch latest responses
            responses = await self.google_forms.get_latest_responses(
                GOOGLE_SPREADSHEET_ID,
                'Form Responses 1!A2:H'
            )

            if not responses:
                logger.warning("No responses received from Google Sheets")
                return

            # Process only new responses
            if len(responses) <= self.last_processed_row:
                return

            # Get the applications channel
            channel = self.bot.get_channel(APPLICATIONS_CHANNEL_ID)
            if not channel:
                logger.error(f"Could not find applications channel: {APPLICATIONS_CHANNEL_ID}")
                return
            
            logger.info(f"Processing {len(responses) - self.last_processed_row} new applications")
            
            # Send embeds for new applications
            for i in range(self.last_processed_row, len(responses)):
                response = responses[i]
                await self.send_application_embed(channel, response, i + 1)

            # Update the last processed row
            self.last_processed_row = len(responses)
            
        except Exception as e:
            logger.error(f"Error in process_new_applications: {e}")
            raise

    async def send_application_embed(self, channel, response, application_id):
        try:
            embed = create_application_embed(application_id, response)
            view = ApplicationView(str(application_id))
            await channel.send(embed=embed, view=view)
            logger.info(f"Successfully sent application #{application_id}")
        except Exception as e:
            logger.error(f"Error sending application #{application_id}: {e}")

async def setup(bot):
    await bot.add_cog(Applications(bot))
