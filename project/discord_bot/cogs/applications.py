import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import logging
from ...config import APPLICATIONS_CHANNEL_ID, GOOGLE_SPREADSHEET_ID
from ...utils.google_forms import GoogleFormsAPI
from .views import ApplicationView
from .embeds import create_application_embed

logger = logging.getLogger('discord_bot')

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
            logger.error(f"Error sending application #{application_id}: {e}")
            raise

    @check_applications.before_loop
    async def before_check_applications(self):
        await self.bot.wait_until_ready()
