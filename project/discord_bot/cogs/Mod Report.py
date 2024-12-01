import discord
from discord.ext import commands
from config import MOD_ROLE_ID, MOD_SUPPORT_CHANNEL_ID

class Officer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Officer'])
    async def officer(self, ctx):
        """
        Ping officers for help in the support channel
        Usage: !officer or !Officer
        """
        # Get the support channel
        support_channel = self.bot.get_channel(1196120590243856544)
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

async def setup(bot):
    await bot.add_cog(Officer(bot))
