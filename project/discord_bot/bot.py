import asyncio
import discord
from discord.ext import commands
from config import TOKEN, COMMAND_PREFIX
from utils.logger import setup_logger
from flask import Flask
import threading

logger = setup_logger()
# Flask setup
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# Call keep_alive() before bot runs
keep_alive()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
        self.logger = logger

    async def setup_hook(self):
        try:
            # Load all cogs
            await self.load_extension('cogs.greetings')
            await self.load_extension('cogs.utilities')
            await self.load_extension('cogs.officer')    # Updated
            await self.load_extension('cogs.deployment') # Updated
            await self.load_extension('utils.error_handler')
            self.logger.info('All extensions loaded successfully')
        except Exception as e:
            self.logger.error(f'Error loading extensions: {str(e)}')
            raise
        
    async def on_ready(self):
        self.logger.info(f'{self.user} has connected to Discord!')
        self.logger.info(f'Bot is in {len(self.guilds)} guilds')

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

