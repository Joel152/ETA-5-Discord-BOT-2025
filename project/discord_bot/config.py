import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '!'

# Add these IDs from your Discord server
OFFICER_ROLE_ID = int(os.getenv('OFFICER_ROLE_ID', '123456789'))  # Replace with actual officer role ID
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', '987654321'))  # Replace with actual support channel ID
DEPLOYMENT_ROLE_ID = int(os.getenv('DEPLOYMENT_ROLE_ID', '123456789'))  # Replace with actual deployment role ID
DEPLOYMENT_CHANNEL_ID = int(os.getenv('DEPLOYMENT_CHANNEL_ID', '987654321'))  # Replace with actual deployment channel ID

# Channel IDs
WELCOME_CHANNEL_ID = int(os.getenv('1081801136719282198'))
FAREWELL_CHANNEL_ID = int(os.getenv('1081801136719282198'))
MODERATION_CHANNEL_ID = int(os.getenv('1313875777976008825'))
MODERATION_THREAD_ID = int(os.getenv('1313875920511303730'))
REPORTS_CHANNEL_ID = int(os.getenv('1313875777976008825'))

# Role IDs
MOD_ROLE_ID = int(os.getenv('1202649275130183760'))