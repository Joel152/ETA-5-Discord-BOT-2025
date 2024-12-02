from .applications import application

async def setup(bot):
    await bot.add_cog(Applications(bot))
