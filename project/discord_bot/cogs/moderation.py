import discord
from discord.ext import commands
from config import OFFICER_ROLE_ID, SUPPORT_CHANNEL_ID, DEPLOYMENT_ROLE_ID, DEPLOYMENT_CHANNEL_ID
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Officer'])
    async def officer(self, ctx):
        """
        Ping officers for help in the support channel
        Usage: !officer or !Officer
        """
        # Get the support channel
        support_channel = self.bot.get_channel(1112369312049668126)
        if not support_channel:
            await ctx.send("Error: Support channel not found. Please contact an administrator.")
            return

        # Get the officer role
        officer_role = ctx.guild.get_role(1105383688738439238)
        if not officer_role:
            await ctx.send("Error: Officer role not found. Please contact an administrator.")
            return

        # Create message with user mention, channel link, and officer ping
        message = (
            f"{ctx.author.mention} needs help in {ctx.channel.mention}\n"
            f"{officer_role.mention}"
        )

        # Send the message in the support channel
        await support_channel.send(message)
        
        # Confirm to the user
        await ctx.send(f"Officers have been notified and will assist you soon!")

    @commands.command()
    @commands.has_role(1105383688738439238)
    async def dep(self, ctx):
        """
        Create a deployment poll
        Usage: !dep
        Required role: Deployment role
        """
        # Get the deployment channel
        deployment_channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not deployment_channel:
            await ctx.send("Error: Deployment channel not found. Please contact an administrator.")
            return

        # Create the deployment poll message
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        message = (
            "Deployment Poll\n"
            "------------------------------\n"
            f"Deployment?\n"
            f"Host: {ctx.author.mention}\n"
            "------------------------------\n"
            "Site?\n"
            "Site-45: :Yes~2:\n"
            "------------------------------\n"
            "3+ reactions\n"
            f"Time: {current_time}\n"
            f"Date: {current_date}\n"
            "------------------------------\n"
            "Vote below."
        )

        # Send the message and add the initial reaction
        poll_message = await deployment_channel.send(message)
        await poll_message.add_reaction('✅')
        
        # Confirm to the user
        await ctx.send(f"Deployment poll created in {deployment_channel.mention}")

    @dep.error
    async def dep_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"You need the deployment role to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))