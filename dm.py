import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Needed to DM members

bot = commands.Bot(command_prefix=";", intents=intents)

REQUIRED_ROLE_ID = 1315151378632540230

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="dm", description="miel only")
@app_commands.describe(user="who's going to be dmed")
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def dm(interaction: discord.Interaction, user: discord.Member):
    try:
        await user.send("_ _\n\n\n\n\n_ _        *sep  over.*   ﹙   <a:emoji_4:1315006475978149950>   ﹚   {user.mention}     ✿\n-# _ _         check invites    .    ◟⠀run **`/breakup`** in ticket\n\n\n\n\n_ _")
        await interaction.response.send_message("user has been dmed", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't DM that user. They might have DMs off.", ephemeral=True)

@dm.error
async def dm_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

bot.run('TOKEN')
