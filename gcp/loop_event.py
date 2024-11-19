from discord.ext import tasks

class loop_event:
    @tasks.loop(seconds=20)
    async def leave_if_alone(self):
        for vc in self.client.voice_clients:
            if len(vc.channel.members) == 1:
                await vc.disconnect()

    @leave_if_alone.before_loop
    async def before_leave_if_alone(self):
        await self.client.wait_until_ready()