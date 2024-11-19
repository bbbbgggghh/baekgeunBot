import discord
from discord.ext import commands
import asyncio
from tokens import Token
import play, playlist, autoplay, etc_commands, loop_event

intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True

class geunBot(commands.Cog, play.play, playlist.playlist, autoplay.autoplay,
              etc_commands.etc_commands, loop_event.loop_event):
    def __init__(self, client):
        self.client = client
        self.leave_if_alone.start()
        self.queue = []
        self.playlist = False
        self.playlist_entries = []
        self.playlist_index = []
        self.is_stopping = False
        self.current_song = None
        self.current_url = None
        self.autoplay = False
        self.autoplay_try = 0
        self.is_crawling = False
        self.is_cover = False
        self.prev_title = []
        self.repeat = False

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="안녕하세요. !help"))
    channel = client.get_channel("my channel id")
    await channel.send("ㅎㅇ용")

@client.event
async def on_message(message):
    if message.content.startswith("!"):
        await client.process_commands(message)
        await asyncio.sleep(1)
        await message.delete()
    elif message.author == client.user:
        await asyncio.sleep(10)
        await message.delete()

async def main():
    await client.add_cog(geunBot(client))
    await client.start(Token)

asyncio.run(main())
