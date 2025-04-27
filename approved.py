import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="a")
async def approve(ctx):
    await ctx.send("_ _\n\n　　　　𝜗 　[**checkpoints required**]( https://discord.gg/SAzqaQuCQA )\n　　　　don't join if not posting yet\n-# _ _　　　⠀  **1w  to  post  ask  4  ext.**　<a:freedom:1350041904099889182> 　୧\n\n_ _")

bot.run(TOKEN)
