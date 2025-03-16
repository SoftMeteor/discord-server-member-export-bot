# ============ BOT CONFIGURATION ============
# Replace this with your actual Discord bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Replace with server ID for faster and server specific command sync
# Set to None to register command to all servers (may take hours to sync)
# Example: SPECIFIED_GUILD_ID = "123456789012345678"
SPECIFIED_GUILD_ID = None
# ==========================================





!pip install discord.py pandas

import os
import discord
from discord import app_commands
import pandas as pd
from datetime import datetime
from io import StringIO
import asyncio
from google.colab import files
from IPython.display import display, HTML



# Setup
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

specified_guild = discord.Object(id=SPECIFIED_GUILD_ID) if SPECIFIED_GUILD_ID else None



# Sync command
@client.event
async def on_ready():
    print(f"\n=== Bot is online as {client.user} ===")
    
    if specified_guild:
        tree.copy_global_to(guild=specified_guild)
        await tree.sync(guild=specified_guild)
        print(f"Synced commands to server: {SPECIFIED_GUILD_ID}")
    else:
        await tree.sync()
        print("Synced commands globally. This may take some time.")
    
    print("Bot is running. Keep this Colab cell running.")

@tree.command(
    name="exportmembers",
    description="Export all server members to a CSV file (Admin only)"
)
@app_commands.checks.has_permissions(administrator=True)



# Export members list to CSV
async def export_members(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    
    try:
        guild = interaction.guild
        
        members = []
        async for member in guild.fetch_members(limit=None):
            members.append(member)
        
        members_data = []
        for member in members:
            roles = [role.name for role in member.roles if role.id != guild.id]
            roles_str = "; ".join(roles)
            
            display_name = member.display_name if hasattr(member, 'display_name') else member.name
            
            # Export data
            members_data.append({
                "ID": member.id,
                "Display Name": display_name,
                "Username": member.name,
                "Nickname": member.nick if member.nick else "",
                "Roles": roles_str,
                "Joined At": member.joined_at.isoformat() if member.joined_at else "",
                "Created At": member.created_at.isoformat(),
                "Tag": str(member),
                "Discriminator": member.discriminator,
                "Bot": "Yes" if member.bot else "No"
            })
        
        df = pd.DataFrame(members_data)
        
        # Sort and separate
        df['Joined At Temp'] = pd.to_datetime(df['Joined At'], errors='coerce')

        users_df = df[df['Bot'] == "No"].sort_values('Joined At Temp')
        bots_df = df[df['Bot'] == "Yes"].sort_values('Joined At Temp')
        
        sorted_df = pd.concat([users_df, bots_df])
        
        sorted_df = sorted_df.drop('Joined At Temp', axis=1)
        
        # Save csv in memory
        guild_name = "".join(c if c.isalnum() else "_" for c in guild.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{guild_name}_members_{timestamp}.csv"
        
        csv_buffer = StringIO()
        sorted_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Display DataFrame
        print("\nMember Data Preview:")
        display(sorted_df.head(10))
        
        with open(filename, 'w') as f:
            f.write(csv_buffer.getvalue())
        
        files.download(filename)
        
        await interaction.followup.send(
            content=f"Exported {len(members_data)} members to CSV.",
            file=discord.File(fp=StringIO(csv_buffer.getvalue()), filename=filename)
        )
        
        print(f"\nExported {len(members_data)} members to CSV. Download started automatically.")
        
    except Exception as e:
        print(f"Error exporting members: {e}")
        await interaction.followup.send(f"An error occurred while exporting members: {str(e)}")

# Missing permissions handler
@export_members.error
async def export_members_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You need Administrator permissions to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

# Run the bot
async def run_bot():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\nERROR: You need to replace \"YOUR_BOT_TOKEN_HERE\" with your actual Discord bot token!")
        return
        
    try:
        print("\nStarting Discord Member Export Bot...")
        await client.start(BOT_TOKEN)
    except discord.errors.LoginFailure:
        print("\nERROR: Invalid Discord bot token. Please check your token and try again.")
    except Exception as e:
        print(f"\nError: {e}")

# Check token and run bot
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("\nERROR: You need to replace \"YOUR_BOT_TOKEN_HERE\" with your actual Discord bot token!")
else:
    # Run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
