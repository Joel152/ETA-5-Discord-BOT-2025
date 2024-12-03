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
        if not any(role.id == APP_READ_ID for role in interaction.user.roles):
            await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
            return

        results_channel = interaction.guild.get_channel(RESULTS_CHANNEL_ID)
        
        embed = discord.Embed(
            title=f"Application {decision.capitalize()}",
            description=f"Application ID: {self.application_id}",
            color=discord.Color.green() if decision == "accepted" else discord.Color.red()
        )
        embed.add_field(name="Decided by", value=interaction.user.mention)
        embed.add_field(name="Decision", value=decision.capitalize())
        embed.timestamp = datetime.now()

        await results_channel.send(embed=embed)
        await interaction.message.edit(view=None)
        await interaction.response.send_message(f"Application {decision}!", ephemeral=True)

def create_application_embed(application_id: int, response: list) -> discord.Embed:
    embed = discord.Embed(
        title=f"New Application #{application_id}",
        color=discord.Color.blue()
    )
    
    # Fields matching your Google Form structure
    embed.add_field(name="Discord Username", value=response[1], inline=False)  # Timestamp is at index 0
    embed.add_field(name="Age", value=response[2], inline=True)
    embed.add_field(name="Region/Timezone", value=response[3], inline=True)
    embed.add_field(name="Previous Experience", value=response[4], inline=False)
    embed.add_field(name="Why Join?", value=response[5], inline=False)
    embed.add_field(name="Availability", value=response[6], inline=False)
    embed.add_field(name="Additional Information", value=response[7] if len(response) > 7 else "None", inline=False)
    
    embed.timestamp = datetime.now()
    
    return embed

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_forms = GoogleFormsAPI('credentials.json')
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
            if not self.google_forms.service:
                await self.google_forms.authenticate()

            responses = await self.google_forms.get_latest_responses(
                GOOGLE_SPREADSHEET_ID,
                'Form Responses 1!A2:H'
            )

            if not responses:
                logger.warning("No responses received from Google Sheets")
                return

            if len(responses) <= self.last_processed_row:
                return

            channel = self.bot.get_channel(APPLICATIONS_CHANNEL_ID)
            if not channel:
                logger.error(f"Could not find applications channel: {APPLICATIONS_CHANNEL_ID}")
                return
            
            logger.info(f"Processing {len(responses) - self.last_processed_row} new applications")
            
            for i in range(self.last_processed_row, len(responses)):
                response = responses[i]
                await self.send_application_embed(channel, response, i + 1)

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
            logger.error(f"Error sending application #{applicati
