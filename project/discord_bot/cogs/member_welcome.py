import discord
from discord.ext import commands

class MemberWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            welcome_dm = (
                f"👋 Welcome to ETA-5 \"Jäeger Bombers\", {member.name}!\n\n"
                "We're excited to have you join our community. Here's some important information:\n\n"
                "📌 **Getting Started**:\n"
                "1. Read our rules and guidelines in the information channel\n"
                "2. Set up your roles by following the verification process\n"
                "3. Introduce yourself in the community chat\n\n"
                "🔧 **Need Help?**\n"
                "Feel free to ask questions in our help channels or contact our staff members.\n\n"
                "🌟 **Quick Links**:\n"
                "• Rules: Check the information channel\n"
                "• Support: Use the !officer command in any channel\n"
                "• Website: https://sites.google.com/view/eta-5-jaegerbombers/home\n\n"
                "We hope you enjoy your time here!"
            )

            # Create an embed for the DM
            embed = discord.Embed(
                title="Welcome to ETA-5 \"Jäeger Bombers\"!",
                description=welcome_dm,
                color=discord.Color.gold()
            )
            embed.set_footer(text="If you have any questions, don't hesitate to ask!")

            # Send the DM to the new member
            await member.send(embed=embed)

        except discord.Forbidden:
            # Log if we couldn't send the DM (e.g., user has DMs disabled)
            print(f"Could not send welcome DM to {member.name} - DMs may be disabled")
        except Exception as e:
            print(f"Error sending welcome DM to {member.name}: {e}")

async def setup(bot):
    await bot.add_cog(MemberWelcome(bot))
