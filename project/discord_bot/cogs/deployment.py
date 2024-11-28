import discord
from discord.ext import commands
from config import DEPLOYMENT_ROLE_ID, DEPLOYMENT_CHANNEL_ID
from datetime import datetime

class Deployment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(1105383688738439238)
    async def dep(self, ctx):
        """
        Create a deployment poll
        Usage: !dep
        Required role: Deployment role
        """
        # Get the deployment channel
        deployment_channel = self.bot.get_channel(1091568165147906098)
        if not deployment_channel:
            await ctx.send("Error: Deployment channel not found. Please contact an administrator.")
            return

        # Create the deployment poll embed
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")

        embed = discord.Embed(
            title="Deployment Poll",
            description="Vote below.",
            color=discord.Color.black()
        )
        embed.add_field(
            name="Deployment?",
            value=f"Host: {ctx.author.mention}",
            inline=False
        )
        embed.add_field(
            name="Site?",
            value="Site-45: :Yes~2:",
            inline=False
        )
        embed.add_field(
            name="Reactions Needed",
            value="3+ reactions",
            inline=False
        )
        embed.set_footer(text=f"Time: {current_time} | Date: {current_date}")
        
        # Send the embed message and add the initial reaction
        poll_message = await deployment_channel.send(embed=embed)
        await poll_message.add_reaction('✅')
        
        # Confirm to the user
        await ctx.send(f"Deployment poll created in {deployment_channel.mention}")

    @dep.error
    async def dep_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You need the deployment role to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Deployment(bot))
