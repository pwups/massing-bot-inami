import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_CHANNEL_ID = 1318526765710184488

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
        placeholder="batch / 1h / 2h / ovn || ovn = urg paids only",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        current_channel = interaction.channel
        sep_time = self.sep_time.value
        urgency = self.urgency.value
        notification = self.notification.value

        target_channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            await target_channel.send(f"\n_ _               (｡˙ヮ˙) ⠀ׂ   ִ    **{sep_time}** ⠀<a:cd_gif:1365839721057620021> ⠀{user.mention}\n_ _               **{urgency}**⠀ヽ⠀**{notification}**⠀ヽ⠀{current_channel.mention}\n_ _")

# Rename the current channel
        try:
            await current_channel.edit(name=f"{sep_time}．{user.name}")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to edit the channel name.", ephemeral=True)
            return

        await interaction.response.send_message("_ _\n\n_ _ ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀[*queued*](https://discord.com/channels/1314982962919379044/1318526765710184488)⠀♡\n_ _  ⠀  ⠀ ⠀⠀⠀⠀ ⠀⠀⠀⠀ *check  pings  &  dms.*\n\n_ _", ephemeral=False)

class ClickMeView(discord.ui.View):
    @discord.ui.button(label="ㅤtook me out to the ballet . . .ㅤ", style=discord.ButtonStyle.secondary)
    async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NotificationModal())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="nobody", description="only like myself when i'm with you . . .")
async def nobody(interaction: discord.Interaction):
    embed = discord.Embed()
    embed.set_image(url="https://hiphophundred.com/wp-content/uploads/2022/12/Screen-Shot-2022-12-16-at-1.02.56-PM.png")

    await interaction.response.send_message(
        content="<:b_blank001:1349341503163732091>\nㅤㅤㅤㅤ<:emoji_2:1315004719063760917>ㅤnobody  gets  me  you  doㅤ᧔♡᧓ \n<:b_blank001:1349341503163732091>",
        embed=embed,
        view=ClickMeView()
    )

bot.run(TOKEN)
