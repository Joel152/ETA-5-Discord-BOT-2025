import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# Add these IDs from your Discord server
OFFICER_ROLE_ID = int(os.getenv('OFFICER_ROLE_ID', '1105383688738439238'))  # Replace with actual officer role ID
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', '1196120590243856544'))  # Replace with actual support channel ID
DEPLOYMENT_ROLE_ID = int(os.getenv('DEPLOYMENT_ROLE_ID', '1095665332791824454'))  # Replace with actual deployment role ID
DEPLOYMENT_CHANNEL_ID = int(os.getenv('DEPLOYMENT_CHANNEL_ID', '1091568165147906098'))  # Replace with actual deployment channel ID
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID', '1197904372189888623'))  # Add this line
MOD_SUPPORT_CHANNEL_ID = int(os.getenv('MOD_SUPPORT_CHANNEL_ID', '1251838912662339646'))
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID', '1202649275130183760'))
