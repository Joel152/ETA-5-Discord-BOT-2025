import asyncio
import discord
from discord.ext import commands
from config import TOKEN, COMMAND_PREFIX, PORT
from utils.logger import setup_logger
from webserver import setup_webserver

logger = setup_logger()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
        self.logger = logger
        self.web_server = None

    async def setup_hook(self):
        try:
            # Setup web server first to ensure it's running before bot setup
            self.web_server = await setup_webserver(PORT)
            self.logger.info('Web server initialized successfully')
            
            # Load all cogs
            await self.load_extension('cogs.greetings')
            await self.load_extension('cogs.utilities')
            await self.load_extension('cogs.moderation')
            await self.load_extension('cogs.deployment')
            await self.load_extension('cogs.member_welcome')
            await self.load_extension('cogs.status')
            await self.load_extension('cogs.applications')
            await self.load_extension('utils.error_handler')
            
            # Sync slash commands
            await self.tree.sync()
            
            self.logger.info('All extensions loaded successfully')
        except Exception as e:
            self.logger.error(f'Error during setup: {str(e)}')
            raise
        
    async def on_ready(self):
        self.logger.info(f'{self.user} has connected to Discord!')
        self.logger.info(f'Bot is in {len(self.guilds)} guilds')
        self.logger.info(f'Web server running on port {PORT}')

    async def close(self):
        if self.web_server:
            await self.web_server.cleanup()
        await super().close()

async def main():
    try:
        bot = DiscordBot()
        async with bot:
            await bot.start(TOKEN)
    except Exception as e:
        logger.error(f'Fatal error: {str(e)}')
        raise

if __name__ == "__main__":
    asyncio.run(main())
