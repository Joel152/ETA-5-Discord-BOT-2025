import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
        embed.add_field(name="Server Created", value=guild.created_at.strftime("%B %d, %Y"))
        embed.add_field(name="Member Count", value=guild.member_count)
        embed.add_field(name="Owner", value=guild.owner.mention)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Info", color=member.color)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"))
        embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"))
        embed.add_field(name="Roles", value=" ".join([role.mention for role in member.roles[1:]]))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))