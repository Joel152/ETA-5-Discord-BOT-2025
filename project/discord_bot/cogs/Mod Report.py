import discord
from discord.ext import commands
from config import MOD_ROLE_ID, MOD_SUPPORT_CHANNEL_ID

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dmt'])
    async def officer(self, ctx):
        """
        Ping a Discord Mod for help in the support channel
        Usage: !dmt or !Dmt
        """
        # Get the support channel
        support_channel = self.bot.get_channel(MOD_SUPPORT_CHANNEL_ID)
        if not support_channel:
            await ctx.send("Error: Support channel not found. Please contact an administrator.")
            return

        # Get the officer role
        officer_role = ctx.guild.get_role(MOD_ROLE_ID)
        if not officer_role:
            await ctx.send("Error: Mod role not found. Please contact an administrator.")
            return

        # Create message with user mention, channel link, and officer ping
        message = (
            f"{ctx.author.mention} needs help in {ctx.channel.mention}\n"
            f"{officer_role.mention}"
        )

        # Send the message in the support channel
        await support_channel.send(message)
        
        # Confirm to the user
        await ctx.send(f"Mods have been notified and will assist you soon!")

async def setup(bot):
    await bot.add_cog(dmt(bot))
