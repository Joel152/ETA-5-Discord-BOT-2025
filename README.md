# ETA-5 OS

A modular Discord bot built with discord.py.

## Features

- Welcome message for new members
- Basic commands: !hello, !ping
- Utility commands: !serverinfo, !userinfo
- Moderation commands: !officer
- Deployment commands: !dep

## Setup

1. Create a Discord application and bot at https://discord.com/developers/applications
2. Copy your bot token
3. Update the `.env` file with your:
   - Discord bot token
   - Officer role ID (from your server)
   - Support channel ID (from your server)
   - Deployment role ID (from your server)
   - Deployment channel ID (from your server)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the bot: `python bot.py`

## Commands

- `!hello` - Bot responds with a greeting
- `!ping` - Check bot's latency
- `!serverinfo` - Display server information
- `!userinfo [@user]` - Display user information (defaults to command user if no mention)
- `!officer` - Request help from officers (will ping them in the support channel)
- `!dep` - Create a deployment poll (requires deployment role)

## Project Structure

- `bot.py` - Main bot file with core setup
- `config.py` - Configuration and environment variables
- `cogs/` - Command modules
  - `greetings.py` - Welcome messages and basic commands
  - `utilities.py` - Utility commands
  - `officer.py` - Officer Commands
  - `deployment.py` - Deployment Commands
  - 
