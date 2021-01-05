import discord
from discord.ext import commands 
from discord.utils import get
from datetime import datetime
from discord import Webhook, AsyncWebhookAdapter
from discord.ext.commands import Greedy

from typing import Optional
import time
import asyncio
import json 
import os

#START USED FOR gitignore, so token is not publicly displayed on github
if os.path.exists(os.getcwd() + '/config.json'):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "","Prefix": "#!"}
    with open(os.getcwd() +'/config.json',"w+") as f:
        json.dump(configTemplate,f)
##END USED FOR gitignore, so token is not publicly displayed on github

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(intents=intents,command_prefix = '!',help_command = None,case_insensitive = True)
client.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_BLUE": 0x206694,
    "DARK_RED": 0x992D22,
    "DARK_AQUA": 0x11806A
}
client.color_list = [i for i in client.colors.values()]

token = configData["Token"]
prefix = configData["Prefix"]

## the array here contains any files that are to be included in this main file such as files with Cogs,
extensions = ['Commands']

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension,error))

##### EVENTS runs when bot detects an activity has happened
@client.event
async def on_ready():   # this event checks when bot is ready and online
    await client.change_presence(status = discord.Status.online,activity=discord.Game('Visual Studio Code')) 
    print('Bot is ready.')

@client.event  #this is the event "decorator"
async def on_member_join(member):   # member object
    print(f'{member} has joined the server.')
    channel = get(member.guild.text_channels, name = 'bot-testing')
    await channel.send(f'<@!{member.id}> has entered The Arena.')
    role = get(member.guild.roles, name = 'Peasants')
    await member.add_roles(role)
    print(f"{member} has been given role of 'Peasants'.")

@client.event  #this is the event "decorator"
async def on_member_remove(member):   # member object
    print(f'{member} has been removed from the server.')


@client.event 
async def on_message(message):
    if(str(message.author) != "Experiment Bot#3647"):        # if statement so bot's messages wont print on terminal
        print(f'{message.author} has sent a message to the server in {message.channel} channel: {message.content}')
    if(message.content.casefold() == "warzone"):
        await message.channel.send('https://cdn.discordapp.com/attachments/742818371917053983/773035164182773780/11CD01E0-6C8B-404E-8D9C-76ACD4235276.mp4')
    if(message.content.casefold() == "its time"):
        await message.channel.send('@everyone https://cdn.discordapp.com/attachments/742818371917053983/774819217643536384/Get_In_the_Arena_-_Short.mp4')
    await client.process_commands(message)  

@client.event
async def on_typing(TextChannel,user,time):
    time = datetime.now() # gets the current time from datetime library,
    print(f'{user} has began typing in {TextChannel} at {time}.')

@client.event
async def on_invite_create(invite):
    print(f'{invite} has been created.')
 
client.run(token) 
