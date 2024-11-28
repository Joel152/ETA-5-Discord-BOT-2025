import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Replace with your desired channel ID
        specific_channel_id = YOUR_CHANNEL_ID  # Replace YOUR_CHANNEL_ID with the specific channel ID
        channel = member.guild.get_channel(1197904372189888623)

        if channel:
            # Create the embed for the welcome message
            embed = discord.Embed(
                title='ETA-5 "Jäger Bombers"',
                description=(
                    f"Hello {member.mention}, welcome to ETA-5 \"Jäger Bombers\".\n\n"
                    "Make sure to read the <#CHANNEL_ID_FOR_INFORMATION> :information:\n"
                    "Learn more about us in <#CHANNEL_ID_FOR_GUIDE> :guide:\n"
                    "Ping the host of the tryout and get your role <#CHANNEL_ID_FOR_NON_VERIFIED_CHAT> :non-verified-chat:\n\n"
                    "Please visit our website to learn more about sub-divisions and other related topics:\n"
                    "[ETA-5 Website](https://sites.google.com/view/eta-5-jaegerbombers/home)\n\n"
                    "Welcome to the team."
                ),
                color=discord.Color.black()
            )
            embed.set_image(url="WELCOME_IMAGE_URL")  # Replace with the URL of your welcome image
            embed.set_footer(text='ETA-5 | "Jäger Bombers"', icon_url="https://cdn.discordapp.com/attachments/1060216735992647700/1219298237505339514/image_7.png?ex=67492d39&is=6747dbb9&hm=b5ecc25771973bc5b113847cc06ad05887e7b01b3c1f263f46191cf6a9e7ecbc&")  # Optional footer icon URL

            # Send the embed message to the specific channel
            await channel.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Greetings(bot))
