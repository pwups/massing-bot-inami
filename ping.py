import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True  # Needed to edit channels

bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="d")
async def sep_over(ctx):
    await ctx.send("_ _\n\n\n\n　　　　　　♡　　₊　　*sep  over.*\n　　　　　　run　**` /breakup `**  ৎ\n\n\n\n_ _")

    try:
        await ctx.channel.edit(name="done")
    except discord.Forbidden:
        await ctx.send("I don't have permission to rename the channel.", delete_after=5)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}", delete_after=5)

bot.run(os.getenv("DISCORD_TOKEN"))
