import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# Web Server Configuration
PORT = int(os.getenv('PORT', '10000'))  # Render expects PORT environment variable

# Role and Channel IDs
OFFICER_ROLE_ID = int(os.getenv('OFFICER_ROLE_ID', '123456789'))
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', '987654321'))
DEPLOYMENT_ROLE_ID= int(os.getenv('DEPLOYMENT_ROLE_ID', '123456789'))
DEPLOYMENT_CHANNEL_ID=int(os.getenv('DEPLOYMENT_CHANNEL_ID', '987654321'))
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID', '987654321'))
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID', '123456789'))
MOD_SUPPORT_CHANNEL_ID = int(os.getenv('MOD_SUPPORT_CHANNEL_ID', '987654321'))
