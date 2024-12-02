import discord
from datetime import datetime

def create_application_embed(application_id: int, response: list) -> discord.Embed:
    embed = discord.Embed(
        title=f"New Application #{application_id}",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Discord Username", value=response[0], inline=False)
    embed.add_field(name="Age", value=response[1], inline=True)
    embed.add_field(name="Experience", value=response[2], inline=False)
    embed.add_field(name="Why Join?", value=response[3], inline=False)
    
    embed.timestamp = datetime.now()
    
    return embed
