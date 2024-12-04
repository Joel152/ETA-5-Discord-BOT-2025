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
DEPLOYMENT_PING_ROLE=int(os.getenv('DEPLOYMENT_PING_ROLE', '1166256882583879730'))
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID', '987654321'))
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID', '123456789'))
MOD_SUPPORT_CHANNEL_ID = int(os.getenv('MOD_SUPPORT_CHANNEL_ID', '987654321'))
APP_READ_ID= os.getenv('APP_READ_ID')
APPLICATIONS_CHANNEL_ID= os.getenv('APPLICATIONS_CHANNEL_ID')
RESULTS_CHANNEL_ID= os.getenv('RESULTS_CHANNEL_ID')
GOOGLE_FORM_ID= os.getenv('GOOGLE_FORM_ID')
GOOGLE_SPREADSHEET_ID=os.getenv('GOOGLE_SPREADSHEET_ID')
