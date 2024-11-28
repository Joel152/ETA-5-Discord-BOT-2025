import discord
from discord.ext import commands
from config import WELCOME_CHANNEL_ID

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_image_path = "project/discord_bot/assests/welcome_image.png"  # Path to your welcome image

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get the welcome channel
        welcome_channel = self.bot.get_channel(987654321)
        if not welcome_channel:
            return

        # Create the welcome message
        welcome_text = (
            f"Hello {member.mention} welcome to ETA-5 \"Jäeger Bombers\",\n"
            f"Make sure to read the #📋 information\n"
            f"Learn More about us in #📘 guide\n"
            f"Ping the host of the tryout and get your role #🔮non-verified-chat\n\n"
            f"Please visit our website to learn more about sub-divisions and other related topics.\n"
            f"https://sites.google.com/view/eta-5-jaegerbombers/home?authuser=0\n\n"
            f"Welcome to the team."
        )

        try:
            # Create an embed for a more stylized message
            embed = discord.Embed(
                title="Welcome to ETA-5 \"Jäeger Bombers\"",
                description=welcome_text,
                color=discord.Color.black()
            )

            # Add the welcome image to the embed
            # Replace 'image_url' with your actual image URL or use file attachment
            embed.set_image(url="project/discord_bot/assests/welcome_image.png")

            # Send the welcome message with the image
            await welcome_channel.send(
                file=discord.File(self.welcome_image_path),
                embed=embed
            )
        except Exception as e:
            print(f"Error sending welcome message: {e}")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Greetings(bot))
