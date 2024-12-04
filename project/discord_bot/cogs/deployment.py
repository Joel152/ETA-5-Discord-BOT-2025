import discord
from discord.ext import commands
from datetime import datetime
from config import DEPLOYMENT_ROLE_ID, DEPLOYMENT_CHANNEL_ID, DEPLOYMENT_PING_ROLE

class Deployment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_deployment_poll_embed(self, author) -> discord.Embed:
        """
        Creates an embed for the deployment poll
        
        Args:
            author: The discord.Member who initiated the deployment poll
            
        Returns:
            discord.Embed: The formatted embed for the deployment poll
        """
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")

        embed = discord.Embed(
            title="Deployment Poll",
            description="Vote below.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Deployment?",
            value=f"Host: {author.mention}",
            inline=False
        )
        
        embed.add_field(
            name="Site",
            value="Site-45: ✅",
            inline=False
        )
        
        embed.add_field(
            name="Reactions Needed",
            value="3+ reactions",
            inline=False
        )
        
        embed.set_footer(text=f"Time: {current_time} | Date: {current_date}")
        
        return embed

    @commands.command()
    @commands.has_role(DEPLOYMENT_ROLE_ID)
    async def dep(self, ctx):
        """
        Create a deployment poll
        Usage: !dep
        Required role: Deployment role
        """
        deployment_channel = self.bot.get_channel(DEPLOYMENT_CHANNEL_ID)
        if not deployment_channel:
            await ctx.send("Error: Deployment channel not found. Please contact an administrator.")
            return

        # Create the deployment poll embed
        embed = self.create_deployment_poll_embed(ctx.author)

        # Send the message with role ping and embed together
        poll_message = await deployment_channel.send(
            content=f"<@&{DEPLOYMENT_PING_ROLE}> Deployment?",
            embed=embed
        )
        await poll_message.add_reaction('✅')
        
        await ctx.send(f"Deployment poll created in {deployment_channel.mention}")

    @dep.error
    async def dep_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You need the deployment role to use this command.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Deployment(bot))
