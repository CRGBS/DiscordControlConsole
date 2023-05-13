import discord
import subprocess
import asyncio
from discord import Intents
import time

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


CHANNEL_ID = ur channel id
BOT_TOKEN = "urdiscord token"
process = None # declare process as a global variable


async def open_cmd_window():
    global process # indicate that we are modifying the global variable
    process = await asyncio.create_subprocess_shell(
        'cmd', 
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, # add stderr pipe to read error messages
        creationflags=subprocess.CREATE_NEW_CONSOLE # add creationflags to start cmd window
    )
    print('CMD window is opened:', process is not None)
    
async def read_stdout():
    while True:
        await asyncio.sleep(0.1)
        if process is not None:
            output = await process.stdout.readline()
            if not output:
                continue
            decoded_output = output.decode('utf-8', errors='replace').rstrip()
            print(decoded_output)
            if decoded_output.strip():
                await client.get_channel(CHANNEL_ID).send(decoded_output)
            await asyncio.sleep(0.1)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    global process
    if process is None:
        await open_cmd_window()
    else:
        print('CMD window is opened:', process is not None)
    asyncio.create_task(read_stdout())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        await message.channel.send('helo，i am ur discord console bot')
        cmd = message.content.split(f'<@{client.user.id}>')[1].strip()
        print(f'Received command: {cmd}')
        if process is not None:
            process.stdin.write(cmd.encode('utf-8') + b'\n')
            await process.stdin.drain()

@client.event
async def on_voice_state_update(member, before, after):
    global CHANNEL_ID
    if member == client.user:
        if after.channel is not None:
            CHANNEL_ID = after.channel.id

client.run(BOT_TOKEN)
