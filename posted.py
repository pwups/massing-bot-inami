import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_CHANNEL_ID = 1314983771799294092
REQUIRED_ROLE_ID = 1315151378632540230

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="done", description="miel only")
@app_commands.describe(
    sep="sep time",
    user="who",
    link="invite link",
    edit="w4s"
)
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def done(interaction: discord.Interaction, sep: str, user: discord.User, link: str, edit: discord.TextChannel = None):
    target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)

    if not target_channel:
        await interaction.response.send_message("Target channel not found.", ephemeral=True)
        return

    # Send the messages
    await target_channel.send(f"_ _\n\n_ _                          ₊ ⊹      **{sep}** <a:idk_what_this_is:1365916326048039032> {user.mention}\n\n_ _ ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| {link}")
    await target_channel.send("_ _\n\n\n-# _ _  <a:freedom:1350041904099889182>  (｡˘﹏˘｡)っ  **wait  awhile  to  count  invites**         ***!***\n\n\n_ _")

    # Rename the edit channel if provided
    if edit:
        try:
            await edit.edit(name="w4s")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to rename that channel.", ephemeral=True)
            return

    await interaction.response.send_message("Done!", ephemeral=True)

@done.error
async def done_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

bot.run(TOKEN)
