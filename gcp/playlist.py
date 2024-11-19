import yt_dlp
import random
import asyncio

class playlist:
    async def get_playlist_index(self, url):
        YDL_OPTIONS = {
            'extract_flat': True,
            'skip_download': True
        }
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                video_count = len(info['entries'])
                self.playlist_index = list(range(1, video_count + 1))
                random.shuffle(self.playlist_index)

    async def download_next_song(self, ctx):
        if not self.playlist_index:
            self.playlist_index.clear()
            self.playlist_entries.clear()
            self.playlist = False
            await ctx.send("플레이리스트 끝")

        if self.playlist_entries:
            playlist_url = self.playlist_entries[0]
            start_index = self.playlist_index.pop(0)
            YDL_OPTIONS = {
                'format': 'bestaudio',
                'noplaylist': False,
                'playliststart': start_index,
                'playlistend': start_index,
                'ignoreerrors': True,
                'buffer-size': '2M'
            }
            async with ctx.typing():
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playlist_url, download=False)
                    if 'entries' in info and info['entries']:
                        next_song = info['entries'][0]
                        if next_song:
                            self.queue.append((next_song['url'], next_song['title']))
                            await ctx.send(f"다음 곡 준비 완료: **{next_song['title']}**")
                        else:
                            await ctx.send("비공개 영상 스킵됨")
                            await self.download_next_song(ctx)
                        
        if not ctx.voice_client.is_playing():
            await asyncio.sleep(1)
            await self.play_next(ctx)
