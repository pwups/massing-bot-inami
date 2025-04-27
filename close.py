import discord
from discord import app_commands
from discord.ext import commands

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

@bot.tree.command(name="close", description="miel only")
@app_commands.describe(
    user="who",
    reason="why"
)
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def close(interaction: discord.Interaction, user: discord.Member, reason: str):
    try:
        await user.send(f"_ _\n\n\n⠀⠀`  ╬═  ` ⠀ ₊⠀ <:emoji_5:1315006522727600249> ⠀ **ticket closed**\n⠀   **reason**.  ⠀： ⠀ {reason}\n\n\n_ _")
    except discord.Forbidden:
        await interaction.response.send_message("Couldn't DM the user. They might have DMs off.", ephemeral=True)
        return

    await interaction.response.send_message("Ticket closed and channel will be deleted.", ephemeral=True)

    try:
        await interaction.channel.delete()
    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to delete this channel.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@close.error
async def close_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
