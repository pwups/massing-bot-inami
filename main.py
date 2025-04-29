import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=";", intents=intents)

# IDs
CATEGORY_ID = 1350035164922908714
TARGET_CHANNEL_ID_NOTIFICATION = 1318526765710184488
TARGET_CHANNEL_ID_DONE = 1314983771799294092
TARGET_CHANNEL_ID_TICKET = 1314988692393295922
REQUIRED_ROLE_ID = 1315151378632540230

# Colors
DARK_GRAY = discord.Color.from_str("#2C2F33")
BLUE = discord.Color.from_str("#68829B")

# ----- Lose Modal -----
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
        await interaction.response.defer()
        thread = await self.original_message.create_thread(name="(─‿‿─)")
        embed = discord.Embed(description=f"```{self.server_ad.value}```", color=DARK_GRAY)
        await thread.send(content=self.server_ad.value, embed=embed)
        await thread.send(self.invite_link.value)
        await thread.send(f"# <:x_x:1350030689256476672> {self.type_info.value}")
        await interaction.followup.send(
            "_ \n\n\n _                 *wait*   for   approval <a:typing_chatbubble:1349316060964454482>\n_ _                  *do  not  ping  anyone.*\n\n\n_ _",
            ephemeral=True
        )

class ClickButton(discord.ui.View):
    def __init__(self, original_message):
        super().__init__(timeout=None)
        self.original_message = original_message

    @discord.ui.button(label="ㅤⓘ ㅤ click⠀me ㅤ ⸺♩", style=discord.ButtonStyle.secondary)
    async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LoseModal(self.original_message))

# ----- Notification Modal -----
class NotificationModal(discord.ui.Modal, title="(◠◠ ✿)｡"):
    notification = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤnotification",
        placeholder="ping / dm",
        required=True,
        style=discord.TextStyle.short
    )
    urgency = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤurgency",
        placeholder="don't lie about urgency",
        required=True,
        style=discord.TextStyle.short
    )
    sep_time = discord.ui.TextInput(
        label="゜ㅤ──❀ㅤ.ㅤ  ﾟㅤsepㅤtime",
        placeholder="batch / 1h / 2h / ovn",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user = interaction.user
        current_channel = interaction.channel
        target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID_NOTIFICATION)
        if target_channel:
            await target_channel.send(
                f"_ _\n               (｡˙ヮ˙) ⠀ׂ   ִ    *{self.sep_time.value}* ⠀<a:cd_gif:1365839721057620021> ⠀{user.mention}\n"
                f"_ _               **{self.urgency.value}**⠀ヽ⠀**{self.notification.value}**⠀ヽ⠀{current_channel.mention}\n_ _"
            )
        try:
            await current_channel.edit(name=f"{self.sep_time.value}．{user.name}")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to edit the channel name.", ephemeral=True)
            return

        await interaction.followup.send(
            "_ \n\n _ ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀[*queued*](https://discord.com/channels/1314982962919379044/1318526765710184488)⠀♡\n"
            "_ _  ⠀  ⠀ ⠀⠀⠀⠀ ⠀⠀⠀⠀ *check  pings  &  dms.*\n\n_ _",
            ephemeral=False
        )

class ClickMeView(discord.ui.View):
    @discord.ui.button(label="ㅤtook me out to the ballet . . .ㅤ", style=discord.ButtonStyle.secondary)
    async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NotificationModal())

# ----- Ticket Close Button -----
class RegretButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="ㅤ(っ- ‸ – ς)ㅤ",
        style=discord.ButtonStyle.danger
    )
    async def regret_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "_ _\n\n    <:diamond_line:1366074032709042289>  review  has  been  **sent**  ♡\n     ₊   click button to close ticket\n\n_ _",
            view=CloseTicketView()  # 👈 close button included here
        )
        
# ----- Slash Commands -----
@bot.tree.command(name="lose", description="i don't wanna lose . . .")
async def lose(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    user = interaction.user
    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    if not category:
        await interaction.followup.send("Category not found.")
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_messages=True)
    }

    channel = await guild.create_text_channel(name=f"wait．{user.name}", category=category, overwrites=overwrites)

    embed = discord.Embed(
        description="<:b_blank001:1349341503163732091>\n\nㅤㅤㅤㅤ<:emoji_2:1315004719063760917>ㅤnobody  gets  me  you  doㅤ᧔♡᧓ \n<:b_blank001:1349341503163732091>",
        color=DARK_GRAY
    )
    embed.set_image(url="https://uproxx.com/wp-content/uploads/2022/12/sza-nobody-gets-me-video.jpg")

    view = ClickButton(None)
    message = await channel.send(embed=embed, view=view)
    view.original_message = message

    await interaction.followup.send(
        f"_ \n\n\n _　　　　<:0wb:1315190556875292672>          ⁺     ⊹\n_ _　　　　{channel.mention}\n\n\n_ _"
    )

@bot.tree.command(name="nobody", description="only like myself when i'm with you . . .")
async def nobody(interaction: discord.Interaction):
    embed = discord.Embed()
    embed.set_image(url="https://hiphophundred.com/wp-content/uploads/2022/12/Screen-Shot-2022-12-16-at-1.02.56-PM.png")
    await interaction.response.send_message(
        content="<:b_blank001:1349341503163732091>\nㅤㅤㅤㅤ<:emoji_2:1315004719063760917>ㅤnobody  gets  me  you  doㅤ᧔♡᧓ \n<:b_blank001:1349341503163732091>",
        embed=embed,
        view=ClickMeView()
    )

@bot.tree.command(name="done", description="miel only")
@app_commands.describe(sep="sep time", user="who", link="invite link", edit="ticket channel (optional)")
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def done(interaction: discord.Interaction, sep: str, user: discord.User, link: str, edit: discord.TextChannel = None):
    await interaction.response.defer(ephemeral=True)
    target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID_DONE)
    if not target_channel:
        await interaction.followup.send("Target channel not found.")
        return

    await target_channel.send(f"_ _\n\n                          ₊ ⊹      *{sep}* <a:idk_what_this_is:1365916326048039032> {user.mention}\n\n_ _ [⠀]( {link} )")
    await target_channel.send("_ _\n\n\n-# _ _  <a:freedom:1350041904099889182>  (｡˘﹏˘｡)っ  **wait  awhile  to  count  invites**         ***!***\n\n\n_ _")

    if edit:
        try:
            await edit.edit(name="w4s")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to rename that channel.")
            return

    await interaction.followup.send("Done!")

@bot.tree.command(name="dm", description="miel only")
@app_commands.describe(user="who's going to be DMed")
@app_commands.checks.has_role(REQUIRED_ROLE_ID)
async def dm(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)
    try:
        await user.send("_ \n\n\n\n\n _        sep  over.   ﹙   <a:emoji_4:1315006475978149950>   ﹚   ✿\n-# _ _         check invites    .    ◟⠀run **/breakup** in ticket\n\n\n\n\n_ _")
        await interaction.followup.send("User has been DMed.")
    except discord.Forbidden:
        await interaction.followup.send("I couldn't DM that user. They might have DMs off.")

# ----- Regret Command and Close Ticket View -----
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="", style=discord.ButtonStyle.danger, emoji="<a:hrt_locket:1366073837954793483>", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()  # Acknowledge the click immediately
        await interaction.channel.delete()

@bot.tree.command(
    name="regret",
    description="regret, self-blame, inability to move on . . ."
)
@app_commands.describe(
    invites=". invites gained",
    portals=". other portals that posted",
    type=". server type you massed",
    link=". server invite link"
)
async def regret(
    interaction: discord.Interaction,
    invites: int,
    portals: str,
    type: str,
    link: str
):
    await interaction.response.defer(ephemeral=True)  # just defers, not the message that follows

    user = interaction.user
    guild = interaction.guild

    review_channel = guild.get_channel(TARGET_CHANNEL_ID_TICKET)
    if review_channel is None:
        await interaction.followup.send("Review channel not found.")
        return

    content = f"_ _\n                                **__{invites}__    invites**    ◟︵ ｡\n[⠀]({link})"

    embed = discord.Embed(description=f"(+{portals}p)‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ ‎ཀ‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎‎‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎‎ ‎‎ ‎ ‎ ‎ {type}")
    embed.set_image(url="https://media.discordapp.net/attachments/1365870103102492772/1365925776956063834/Untitled201_20250427134111.png?ex=680fbdc2&is=680e6c42&hm=8ddf1e700f1f42c27f670b720fcec7e123b876fb9d9fec06c87036a3b4eec8cd&=&format=webp&quality=lossless")
    embed.set_footer(
        text=f"{user.name}‎ㅤㅤㅤ‎⟢ㅤㅤㅤthankq for massing",
        icon_url=user.avatar.url if user.avatar else discord.Embed.Empty
    )

    await review_channel.send(content=content, embed=embed)

    await interaction.followup.send(
        view=CloseTicketView()
    )

# ----- Events -----
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)
    activity = discord.Activity(type=discord.ActivityType.listening, name="nobody gets me.")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)

bot.run(TOKEN)
