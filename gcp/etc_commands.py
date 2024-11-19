from discord.ext import commands
import random

class etc_commands:
    @commands.command()
    async def autoplay(self, ctx):
        self.autoplay = not self.autoplay
        status = "활성화" if self.autoplay else "비활성화"
        await ctx.send(f"자동 재생 {status}")

    @commands.command()
    async def repeat(self, ctx):
        self.repeat = not self.repeat
        status = "활성화" if self.repeat else "비활성화"
        await ctx.send(f"대기열 반복 {status}")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
        #if ctx.voice_client and ctx.voice_client.is_playing() and not self.autoplay:
            ctx.voice_client.stop()
            await ctx.send("스킵 ㅇ")
        #if self.autoplay:
         #   await ctx.send("자동 재생일때 스킵 불가 (고장남ㅜ)")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            self.is_stopping = True
            await ctx.voice_client.disconnect()
            await ctx.send("정지 ㅇ 나감")
            self.is_stopping = False

    @commands.command()
    async def now(self, ctx):
        if self.current_song:
            await ctx.send(f"현재 재생 중: **{self.current_song}**")
        else:
            await ctx.send("ㄴ")

    @commands.command()
    async def queue(self, ctx):
        if self.queue:
            queue_list = '\n'.join([f"{i+1}. {title}" for i, (_, title) in enumerate(self.queue) if title])
            await ctx.send(f"현재 대기열 :\n{queue_list}")
        else:
            await ctx.send("대기열 비었음")

    @commands.command()
    async def shuffle(self, ctx):
        if len(self.queue) > 1:
            random.shuffle(self.queue)
            await ctx.send("대기열 셔플 완료 ㅇ")
        else:
            await ctx.send("셔플할 노래가 부족함")

    @commands.command()
    async def remove(self, ctx, position: int):
        if position == -1:
            self.queue.clear()
            await ctx.send("대기열 모두 비움")
        elif 1 <= position <= len(self.queue):
            removed_song = self.queue.pop(position - 1)[1]
            await ctx.send(f"삭제 완료: **{removed_song}**")
            if not self.queue and self.index:
                await self.download_next_song(ctx)
        else:
            await ctx.send("ㅗ")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("일시정지")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("다시 재생")

    @commands.command()
    async def reset(self, ctx):
        self.queue.clear()
        self.playlist = False
        self.playlist_entries.clear()
        self.playlist_index.clear()
        self.is_stopping = False
        self.current_song = None
        self.current_url = None
        self.autoplay = False
        self.autoplay_try = 0
        self.is_crawling = False
        self.is_cover = False
        self.prev_title.clear()
        self.repeat = False
        await ctx.send("리셋 완료")
