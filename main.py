import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with your category ID
CATEGORY_ID = 1350035164922908714

DARK_GRAY = discord.Color.from_str("#2C2F33")

class LoseModal(discord.ui.Modal, title="◝（ᵕᵕ✿）◜"):
    server_ad = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤserverㅤad",
        placeholder="no spoiler walls",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000,
    )
    invite_link = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤinviteㅤlink",
        placeholder="vanities = batch",
        style=discord.TextStyle.short,
        required=True,
        max_length=200,
    )
    type_info = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤpaidㅤtype",
        placeholder="point or invite?",
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )

    def __init__(self, original_message):
        super().__init__()
        self.original_message = original_message

    async def on_submit(self, interaction: discord.Interaction):
        thread = await self.original_message.create_thread(name="(─‿‿─)")

        embed = discord.Embed(description=f"```{self.server_ad.value}```", color=DARK_GRAY)
        await thread.send(content=self.server_ad.value, embed=embed)

        await thread.send(self.invite_link.value)
        await thread.send(f"# <:x_x:1350030689256476672> {self.type_info.value}")

        await interaction.channel.send(
            "_ _\n\n\n_ _                 **wait**   for   approval <a:typing_chatbubble:1349316060964454482>\n_ _                  *do  not  ping  anyone.*\n\n\n_ _"
        )

class ClickButton(discord.ui.View):
    def __init__(self, original_message):
        super().__init__(timeout=None)
        self.original_message = original_message

    @discord.ui.button(label="ㅤⓘ ㅤ click⠀me ㅤ ⸺♩", style=discord.ButtonStyle.secondary)
    async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LoseModal(self.original_message))

@bot.tree.command(name="lose", description="i don't wanna lose . . .")
async def lose(interaction: discord.Interaction):
    guild = interaction.guild
    user = interaction.user

    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    if not category:
        await interaction.response.send_message("Category not found.", ephemeral=True)
        return

    # Permissions: hide from everyone, allow the user
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
    }

    channel_name = f"wait．{user.name}"
    channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)

    embed = discord.Embed(
        description="<:b_blank001:1349341503163732091>\n\nㅤㅤㅤㅤ<:emoji_2:1315004719063760917>ㅤnobody  gets  me  you  doㅤ᧔♡᧓ \n<:b_blank001:1349341503163732091>",
        color=DARK_GRAY
    )
    embed.set_image(url="https://uproxx.com/wp-content/uploads/2022/12/sza-nobody-gets-me-video.jpg?w=640")

    view = ClickButton(None)  # Will assign original_message later

    message = await channel.send(embed=embed, view=view)
    view.original_message = message

    await interaction.response.send_message(
        f"_ _\n\n\n_ _　　　　<:0wb:1315190556875292672>          ⁺     ⊹\n_ _　　　　{channel.mention}\n\n\n_ _",
        ephemeral=True
    )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)

bot.run(os.getenv("DISCORD_TOKEN"))
