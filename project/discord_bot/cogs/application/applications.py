import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
import asyncio
from datetime import datetime
from config import (
    APPLICATIONS_CHANNEL_ID,
    RESULTS_CHANNEL_ID,
    APP_READ_ID,
    GOOGLE_SPREADSHEET_ID
)
from utils.google_forms import GoogleFormsAPI

class ApplicationView(View):
    def __init__(self, application_id: str):
        super().__init__(timeout=None)
        self.application_id = application_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        await self.process_decision(interaction, "accepted")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny")
    async def deny_button(self, interaction: discord.Interaction, button: Button):
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
            'Form Responses 1!A2:E'  # Adjust range based on your form
        )

        if len(responses) <= self.last_processed_row:
            return

        channel = self.bot.get_channel(APPLICATIONS_CHANNEL_ID)
        
        for i in range(self.last_processed_row, len(responses)):
            response = responses[i]
            await self.send_application_embed(channel, response, i + 1)

        self.last_processed_row = len(responses)

    async def send_application_embed(self, channel, response, application_id):
        # Adjust field names based on your form structure
        embed = discord.Embed(
            title=f"New Application #{application_id}",
            color=discord.Color.blue()
        )
        
        # Customize these fields based on your form
        embed.add_field(name="Discord Username", value=response[0], inline=False)
        embed.add_field(name="Age", value=response[1], inline=True)
        embed.add_field(name="Experience", value=response[2], inline=False)
        embed.add_field(name="Why Join?", value=response[3], inline=False)
        
        embed.timestamp = datetime.now()
        
        view = ApplicationView(str(application_id))
        await channel.send(embed=embed, view=view)

    @check_applications.before_loop
    async def before_check_applications(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Applications(bot))
