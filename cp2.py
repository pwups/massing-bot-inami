import discord
from discord.ext import commands

TOKEN = os.get.env("TOKEN")

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

    # Autoresponder for "freaky"
    if message.content.lower() == "freaky":
        await message.channel.send("_ _\n\n　　**pls send an eren gif heh.**　·　<:freaky:1365898553578487808>\n\n_ _")

    # Process commands after handling messages
    await bot.process_commands(message)

# Run the bot with your token
bot.run(TOKEN)
