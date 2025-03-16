
# Export Discord server member to .csv (Bot)

Easily export list of Discord server members to a .csv file with no  user limit.\
.cvs file can be open in Excel, Numbers, and Google Sheet

## Setup Discord Bot

**Creating bot**
- Go to [Discord deverloper portal](https://discord.com/developers/applications)
- Click “New Application”
- Click on “Bot” setting (on the left)
- Scroll down to “Privileged Gateway Intents”
- Turn on “SERVER MEMBERS INTENT”

**Inviting bot**
- Go to “OAuth2” (on the left)
- Scroll down to “OAuth2 URL Generator” and select “Bot”
- Scroll down to “BOT PERMISSIONS” and select “Use Slash Command”
- Invite link will be in “GENERATED URL” section

**Getting bot token**
- Click on “Bot” setting (on the left)
- Click “Reset Token”

## Run Locally

**Requirement**
- [Python](https://www.python.org/)
- *Required packages install automatically*

**Running the bot**
- Download and open [Main.py](Main.py) with your text-editor of choice
- Edit 3rd line to your bot token
- *Edit 8th to your server ID (optional but recommended)*
- Save, close, open main.py

**Stopping the bot**
- Press **control +  c** or just close the window



## Run on Google Colab
- Go to [Google Colab](https://colab.research.google.com)
- Create a new notebook
- Paste the code from [Colab.ipynb](Colab.ipynb)
- Edit 3rd line to your bot token
- *Edit 8th to your server ID (optional but recommended)*
- Click run (play icon on the left of the code block)
## Usage

In any text channel, use slash command
```
  /exportmembers
```
