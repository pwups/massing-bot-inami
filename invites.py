import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=";", intents=intents)

TARGET_CHANNEL_ID = 1314988692393295922

BLUE = discord.Color.from_str("#68829B")

class CloseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.danger, emoji='<:Locked:1365926484736475158>', label=None)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        await interaction.channel.delete()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="regret", description="regret, self-blame, inability to move on . . .")
@app_commands.describe(
    invites="﹒　invites gained",
    portals="﹒　other portals that posted",
    link="﹒　server invite link",
    type="﹒　server type you massed (2-3 keywords)"
)
async def regret(interaction: discord.Interaction, invites: int, portals: int, link: str, type: str):
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel is None:
        await interaction.response.send_message("Target channel not found.", ephemeral=True)
        return

  embed = discord.Embed(description=f"(+{portals}p)‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ ‎ཀ‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ {type}", color=BLUE())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1365870103102492772/1365925776956063834/Untitled201_20250427134111.png?ex=680f1502&is=680dc382&hm=3f817d4a8e8dfcaa5925273de06aa3dba6f7e1a44c558fdf25c4cc90c10d7d62")
    embed.set_footer(text=f"{interaction.user.name}‎ㅤㅤㅤ‎⟢ㅤㅤㅤthanks for massing", icon_url=interaction.user.display_avatar.url)

    await target_channel.send(f"‎_ _\n                                **__{invites}__    invites**    ◟︵ ｡\n||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||||‍||
{link}", embed=embed)

    view = CloseButton()

    await interaction.response.send_message("click button to close ticket", view=view)

bot.run(TOKEN)
