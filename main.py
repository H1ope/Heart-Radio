YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch',
    'source_address': '0.0.0.0'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send("You need to join a voice channel first!")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()

    async with ctx.typing():
        try:
            loop = asyncio.get_event_loop()
            # Performs SoundCloud search without touching YouTube
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"scsearch:{search}", download=False))

            if 'entries' in data and len(data['entries']) > 0:
                data = data['entries'][0]

            filename = data['url']
            title = data.get('title', 'Song')

            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            source = discord.FFmpegPCMAudio(
                filename,
                before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                options='-vn'
            )
            ctx.voice_client.play(source)

            await ctx.send(f'Now playing: {title} ')
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

bot.run(os.environ.get('DISCORD_TOKEN'))
