# ============ BOT CONFIGURATION ============
# Replace this with your actual Discord bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Replace with server ID for faster and server specific command sync
# Set to None to register command to all servers (may take hours to sync)
# Example: SPECIFIED_GUILD_ID = "123456789012345678"
SPECIFIED_GUILD_ID = None
# ==========================================




import sys
import subprocess
import importlib.util
import os
import site
from datetime import datetime

# Add user site-packages to path
sys.path.append(site.getusersitepackages())

# Check and install packages
REQUIRED_PACKAGES = ["discord.py", "pandas"]

def check_package(package_name):
    """Check if a package is installed"""
    if package_name == "discord.py":
        package_to_check = "discord"
    else:
        package_to_check = package_name
    return importlib.util.find_spec(package_to_check) is not None

def install_packages():
    """Install required packages if not already installed"""
    missing_packages = [pkg for pkg in REQUIRED_PACKAGES if not check_package(pkg)]
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Attempting to install...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("Package installation successful!")
            return True
        except Exception as e:
            print(f"Error installing packages: {e}")
            input("Press Enter to exit...")
            return False
    return True

if not install_packages():
    sys.exit(1)

import discord
from discord import app_commands
import pandas as pd





# Setup
intents = discord.Intents.default()
intents.members = True  # Need this for accessing member data

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
    
    print("Bot is running. Keep this window open to keep the bot running.")
    print("Press Ctrl+C to stop the bot, or just close this window.")

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
            
            # Export data
            members_data.append({
                "ID": member.id,
                "Username": member.name,
                "Discriminator": member.discriminator,
                "Tag": str(member),
                "Bot": member.bot,
                "Nickname": member.nick if member.nick else "",
                "Joined At": member.joined_at.isoformat() if member.joined_at else "",
                "Created At": member.created_at.isoformat(),
                "Roles": roles_str
            })
        
        df = pd.DataFrame(members_data)
        
        os.makedirs("exports", exist_ok=True)
        
        # Create CSV file
        guild_name = "".join(c if c.isalnum() else "_" for c in guild.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/{guild_name}_members_{timestamp}.csv"
        
        # Save CSV to local file
        df.to_csv(filename, index=False)
        
        # Send the file as a followup
        await interaction.followup.send(
            content=f"Exported {len(members_data)} members to CSV.",
            file=discord.File(filename, filename=f"{guild_name}_members.csv")
        )
        
        print(f"Exported {len(members_data)} members from {guild.name} to {filename}")
        
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



# Run bot
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\nERROR: You need to replace \"YOUR_BOT_TOKEN_HERE\" with your actual Discord bot token!")
        print("Open this file in a text editor and replace the token at line 7.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    try:
        print("\nStarting Discord Member Export Bot...")
        client.run(BOT_TOKEN)
    except discord.errors.LoginFailure:
        print("\nERROR: Invalid Discord bot token. Please check your token and try again.")
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")