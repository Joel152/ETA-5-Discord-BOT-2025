import discord
from discord.ui import Button, View
from datetime import datetime
from config import APP_READ_ID, RESULTS_CHANNEL_ID

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
        if not any(role.id == MOD_ROLE_ID for role in interaction.user.roles):
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
