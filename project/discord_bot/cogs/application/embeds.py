import discord
from datetime import datetime

def create_application_embed(application_id: int, response: list) -> discord.Embed:
    embed = discord.Embed(
        title=f"New Application #{application_id}",
        color=discord.Color.blue()
    )
    
    # Fields matching your Google Form structure
    embed.add_field(name="Discord Username", value=response[1], inline=False)  # Timestamp is at index 0
    embed.add_field(name="Age", value=response[2], inline=True)
    embed.add_field(name="Region/Timezone", value=response[3], inline=True)
    embed.add_field(name="Previous Experience", value=response[4], inline=False)
    embed.add_field(name="Why Join?", value=response[5], inline=False)
    embed.add_field(name="Availability", value=response[6], inline=False)
    embed.add_field(name="Additional Information", value=response[7] if len(response) > 7 else "None", inline=False)
    
    embed.timestamp = datetime.now()
    
    return embed
