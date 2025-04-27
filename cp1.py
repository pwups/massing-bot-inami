import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    # Autoresponder for "rainbow sprinkles"
    if message.content.lower() == "rainbow sprinkles":
        await message.channel.send("_ _\n\n　　**send a song reco**　·　<a:star1:1365889441310179389>\n　　i like = free ovn　✿\n\n_ _")

    # Process commands after handling messages
    await bot.process_commands(message)

# Run the bot with your token
bot.run(TOKEN)
