import discord
from discord.ext import commands
import yt_dlp
import unicodedata

FFMPEG_OPTIONS = {'options': '-vn', 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -threads 1'}

class play:
    @commands.command()
    async def play(self, ctx, *, search=None):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            await ctx.send("음성 채널 입장하고 ㄱㄱㄱ")
        if not ctx.voice_client:
            await voice_channel.connect()

        if search:
            async with ctx.typing():
                if "/playlist" in search or "soundcloud" in search:
                    self.playlist = True
                    self.playlist_entries.append(search)
                    await ctx.send(f'플레이리스트 추가됨')
                    await self.get_playlist_index(search)
                    await self.download_next_song(ctx)

                else:
                    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'buffer-size': '2M'}) as ydl:
                        info = ydl.extract_info(search, download=False) if "https://" in search else ydl.extract_info(f"ytsearch:{search}", download=False)
                        if 'entries' in info:
                            info = info['entries'][0]
                        url = info['url']
                        title = info['title']
                        if self.autoplay:
                            self.prev_title.append(title)
                            if 'cover' in unicodedata.normalize('NFKC', title).lower() or '커버' in unicodedata.normalize('NFKC', title).lower():
                                self.is_cover = True
                            else:
                                self.is_cover = False
                        self.queue.append((url, title))
                        await ctx.send(f'음악 추가됨: **{title}**')

                    if self.autoplay:
                        with yt_dlp.YoutubeDL({'extract_flat': True}) as ydl:
                            info = ydl.extract_info(search, download=False) if "https://" in search else ydl.extract_info(f"ytsearch:{search}", download=False)
                            if not "https://" in search and 'entries' in info:
                                info = info['entries'][0]['url']
                            elif "https://" in search:
                                info = search + "&gl=JP"
                            self.current_url = info
                            await self.play_next(ctx)

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue and not self.is_stopping:
            url, title = self.queue.pop(0)
            self.current_song = title
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'**{title}** 재생 중')

            if self.repeat:
                self.queue.append((url, title))

            if self.playlist:
                await self.download_next_song(ctx)

            if self.autoplay:
                await self.autoplay_recommended(ctx)

        elif not self.queue and not ctx.voice_client.is_playing():
            self.current_song = None
            await ctx.send("재생목록 없음")