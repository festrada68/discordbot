import discord
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.utils import get
from typing import Optional
from discord import Webhook, AsyncWebhookAdapter
import asyncio
from valorant import *
import random

class Commands(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.prefix = self.client.command_prefix
    @commands.command(name = 'help',aliases = ['h','commands'], brief = 'This is the help command!.',description = 'This is the help command, where a list of available commands will be shown.')
    async def help(self,ctx,command = None):
        author = ctx.message.author 
        dm_author = await ctx.message.author.create_dm()
        helpEmbed = discord.Embed(color = random.choice(self.client.color_list))

        def find(command):
            for i in commands:
                if(i.name in command):
                    return i
        ###TODO 
        if(command == None):
            cogs = [i for i in self.client.cogs.keys()]
            for cog in cogs:
                commandList = ""
                for commands in self.client.get_cog(cog).walk_commands():
                    commandList += f"**{self.prefix}{commands.name}** - *{commands.brief}*\n"
                commandList += "\n"
                helpEmbed.add_field(name = cog,value = commandList,inline = False)
                helpEmbed.set_footer(text = f"For a specific command, use {self.prefix}command to get more information on a command.")
                #helpEmbed.set_thumbnail(url = self.client.user.avatar_url)
                helpEmbed.set_thumbnail(url = 'https://i.imgur.com/0Cudu76.jpg?fb')
            await dm_author.send(embed = helpEmbed)
            #await ctx.send(embed = helpEmbed)

        else:
            cogs = self.client.get_cog('Commands')
            commands = cogs.get_commands()
            command = find(command)
            helpEmbed.add_field(name = f"{self.prefix}{command}", value = f"*Description - {command.description}*\nAliases - {command.aliases}",inline = False)
            await dm_author.send(embed = helpEmbed)
            
    @commands.command(brief = 'This is the ping command.',description = 'This gets the client latency running on a host machine.')
    async def ping(self,ctx): 
        await ctx.send(f'This is the ping command! Response time is {round(self.client.latency*1000)}ms')

    @commands.command(name = 'length',aliases = ['len'],brief = 'Gets the length of a message.',description = 'This command is used when testing certain messages.') 
    async def length(self,ctx):
        await ctx.send('**Your message is {} characters long, including spaces.**'.format(len(ctx.message.content) - 8))

    @commands.command(name = "delete",
     aliases = ["purge"],
     brief = 'Deletes specified number of messsages.',
     description = f"Quickly deletes specified # of messages for channel which command was called, if no # of messages specified, only 1 message(most recent) will be deleted.") 
    async def clear_messages(self,ctx,targets: Greedy[discord.Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets
        with ctx.channel.typing():
            if(limit > 10):
                limit = 10 
            await ctx.message.delete() # delete the actual commmand call message
            deleted = await ctx.channel.purge(limit=limit, check=_check)
            await ctx.send("Cleared **{}** Messages.".format(len(deleted)),delete_after = 5)


    @commands.command(name = 'ban',aliases = ['getemout'],brief = 'Bans a member from using chat for 20 seconds.', description = "Only members with administrative permissions can use this command.")
    async def add_roles(self,ctx,member: discord.Member = None):
        if member == None:
            await ctx.send(f"You did not specify who to ban.")
        else:
            if ctx.author.guild_permissions.administrator:
                banned = get(member.guild.roles, name='BANNED')
                currentroles = member.roles
                for i in currentroles[1:]:
                    await member.remove_roles(i)
                await member.add_roles(banned)
                await ctx.send((f'**{member}** has been **BANNED** from chat for 20 seconds.'))
                await asyncio.sleep(20)
                await member.remove_roles(banned)

                for j in currentroles[1:]:
                    await member.add_roles(j)
                await ctx.send((f'<@!{member.id}> has learned their lesson not to flap their gums.'))
            else:
                await ctx.send(f'<@!{ctx.author.id}> you do not have permssion to use this command. <:KEKW:793624031479726101>')
 
    @commands.command(name = "echo",brief = 'Echos command message argument to the server.',description = 'Implemented for testing bot messages.')
    async def echodis(self,ctx, message = None):
        if(message == None):
            raise ValueError("Cannot Echo Empty Message.")
        else:
            await ctx.send(message)

    @commands.command(name = 'valorant',aliases = ['val'],brief = "Gets specified player's competitive stats for Valorant." ,description = 'Enter username#tag to get list of valorant competitive stats including agent stats, weapon stats, and player stats.')
    async def VALORANT(self,ctx,*username ):
        if(username == None):
            await ctx.send('Specify a Player with tag to use command.')
        else:
            #player_name = join(username)
            player_name = " ".join(username)
            test = Player(player_name)

            await ctx.send(f'This is {test.usrname}')
            rank = test.player_stats.rank
            if 'Gold' in rank:
                color = 0xc27c0e
            elif 'Silver' in rank:
                color = 0xA7A7A7
            elif 'Bronze' in rank:
                color = 0x804a00
            else:
                color = 0x191970
            playerOV = discord.Embed(title = "Valorant Competitive Overview Stats",
                                    colour = color,
                                    description = f"**__Rank__ -** **{test.player_stats.rank}**"
                                    )
            playerOV.add_field(name = 'KAD Ratio',value = f'{test.player_stats.KAD}',inline = True)
            playerOV.add_field(name = 'K/D Ratio',value = f'{test.player_stats.KD}',inline = True)
            playerOV.add_field(name = 'Wins',value = f'{test.player_stats.totalwins}',inline = True)
            playerOV.add_field(name = 'Kills',value = f'{test.player_stats.totalkills}',inline = True)
            playerOV.add_field(name = 'Headshots',value = f'{test.player_stats.totalhshots}',inline = True)
            playerOV.add_field(name = 'Aces',value = f'{test.player_stats.ACE}',inline = True)
            playerOV.set_author(name = player_name,icon_url = test.agents.imgs[0])
            playerOV.set_thumbnail(url=test.player_stats.rank_img)
            await ctx.send(embed = playerOV)
            agents = discord.Embed(title = f"Top {test.agents.get_len()} Agent Stats",
                                    colour = 0xB01B1B
                                    )
            for i in range(test.agents.get_len()):
                agents.add_field(name = f'__{test.agents.names[i]}__',value = f'```Time Played: {test.agents.agent_stats[i][0]}\nWin% : {test.agents.agent_stats[i][1]}\nK/D: {test.agents.agent_stats[i][2]}\nDmg/Rnd: {test.agents.agent_stats[i][3]}```' ,inline = True)
            
            agents.set_author(name = player_name,icon_url = test.agents.imgs[0])
            agents.set_thumbnail(url=test.agents.imgs[0])
            await ctx.send(embed = agents)

            weapons = discord.Embed(title = f"Top {test.weapons.get_len()} Weapon Stats",
                                    colour = 0x00CCC0
                                    )
            for i in range(test.weapons.get_len()):
                weapons.add_field(name = f'__{test.weapons.names[i]}__',value = f'```Kills: {test.weapons.Kills[i]}\nHeadshot%: {test.weapons.stats[i][0]}\nBodyshot%: {test.weapons.stats[i][1]}\nLegshot%: {test.weapons.stats[i][2]}```' ,inline = True)
            
            weapons.set_author(name = player_name,icon_url = test.agents.imgs[0])
            weapons.set_thumbnail(url=test.weapons.imgs[0])
            await ctx.send(embed = weapons)

def setup(client):
    client.add_cog(Commands(client))
