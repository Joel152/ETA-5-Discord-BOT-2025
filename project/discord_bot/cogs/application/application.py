import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime

from config import APPLICATIONS_CHANNEL_ID, GOOGLE_SPREADSHEET_ID
from utils.google_forms import GoogleFormsAPI
from .views import ApplicationView
from .embeds import create_application_embed

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google_forms = GoogleFormsAPI('credentials.json')
        self.last_processed_row = 0
        self.check_applications.start()

    def cog_unload(self):
        self.check_applications.cancel()

    @tasks.loop(minutes=5)
    async def check_applications(self):
        try:
            await self.process_new_applications()
        except Exception as e:
            print(f"Error checking applications: {e}")

    async def process_new_applications(self):
        if not self.google_forms.service:
            await self.google_forms.authenticate()

        responses = await self.google_forms.get_latest_responses(
            SPREADSHEET_ID,
            'Form Responses 1!A2:H'  # Updated range to include all fields
        )

        if len(responses) <= self.last_processed_row:
            return

        channel = self.bot.get_channel(APPLICATIONS_CHANNEL_ID)
        
        for i in range(self.last_processed_row, len(responses)):
            response = responses[i]
            await self.send_application_embed(channel, response, i + 1)

        self.last_processed_row = len(responses)

    async def send_application_embed(self, channel, response, application_id):
        embed = create_application_embed(application_id, response)
        view = ApplicationView(str(application_id))
        await channel.send(embed=embed, view=view)

    @check_applications.before_loop
    async def before_check_applications(self):
        await self.bot.wait_until_ready()
