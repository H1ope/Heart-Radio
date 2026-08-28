import os
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
    'quiet': True
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play', help='Plays a song from YouTube, Spotify, or SoundCloud')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel first!")
        return

    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()

    async with ctx.typing():
        if "spotify.com" in search:
            search = f"ytsearch:{search}"

        info = ytdl.extract_info(search, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        url = info['url']
        title = info.get('title', 'Song')

        source = await discord.FFmpegOpusAudio.from_probe(url, FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

    await ctx.send(f" Now playing: {title}**")

@bot.command(name='stop', help='Stops the music and leaves the voice channel')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Playback stopped and disconnected.")

bot.run(os.getenv('DISCORD_TOKEN'))
