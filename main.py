import discord
from discord.ext import commands
import yt_dlp, os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Online na si {bot.user}!")
    await bot.tree.sync()
                          
@bot.tree.command(name="play", description="Tugtog ka ng kanta!")
async def play(interaction: discord.Interaction, kanta: str):
    await interaction.response.send_message(f"🔍 Hinahanap ko: {kanta}...")
    if not interaction.user.voice:
        await interaction.followup.send("Pumasok ka muna sa voice channel, bheee!")
        return
    vc = await interaction.user.voice.channel.connect()
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{kanta}", download=False)
        url = info['entries'][0]['url']
        title = info['entries'][0]['title']
    vc.play(discord.FFmpegPCMAudio(url))
    await interaction.followup.send(f"🎵 Ngayon tumutugtog: **{title}**")

@bot.tree.command(name="stop", description="Stop mo music")
async def stop(interaction: discord.Interaction):

    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Sige, stop na! 😢")
    else:
        await interaction.response.send_message("Wala naman ako tumutugtog eh!")

bot.run(os.getenv("DISCORD_TOKEN")                                              
