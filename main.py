import discord
import requests
import xmltodict
import time, datetime
import random
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from discord_components import DiscordComponents, Button, Select, SelectOption
from cogs.util import store, ready_status

config = store('config.json', None, True)
client = commands.Bot(command_prefix=config['pfx'], help_command=None, owner_ids=config['owner_ids'])
slash = SlashCommand(client)
dcpnt = DiscordComponents(client)
color = hex(random.randint(1118481,16777215))

@client.event
async def on_message_delete(message):
    if message.author.bot: return
    d = store('expose.json', None, True)
    files = []
    if message.attachments != []:
        for file in message.attachments:
            files.append(file.url)
    d[str(message.channel.id)] = {
        "content": message.content,
        "author": f"{message.author}",
        "author_icon": f"{message.author.avatar_url}",
        "files": files
    }
    store('expose.json', d)

@slash.slash(name='color')
async def _color(ctx):
    color = hex(random.randint(1118481,16777215))
    await ctx.channel.send(embed=discord.Embed(title='new color', description='click button below to confirm', color=int(color, base=16)), components=[Button(label='confirm', id=f'conf-{ctx.author.id}-{color}'), Button(label='cancel', id=f'canc-{ctx.author.id}'), Button(label='reroll', id=f'rero-{ctx.author.id}')])

@client.command(aliases=['e'])
@commands.is_owner()
async def expose(ctx):
    try:
        d = store('expose.json', None, True)
        x = d[str(ctx.channel.id)]
    except:
        await ctx.send("nothing to expose!")
        return
    embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), description=x['content'])
    embed.set_author(name=x['author'], icon_url=x['author_icon'])
    embed.set_footer(text='Exposed at')
    if x['files'] != []:
        embed.set_image(url=x['files'][0])
    await ctx.send(embed=embed)
    d.pop(str(ctx.channel.id))
    store('expose.json', d)

@client.event
async def on_button_click(interaction):
    if str(interaction.user.id) != interaction.component.id.split("-")[1]:
        return
    if interaction.component.label == 'cancel':
        await interaction.message.delete()
        return
    if interaction.component.label == 'confirm':
        r = interaction.guild.get_role(751605185725333574)
        await r.edit(colour=int(interaction.component.id.split("-")[2], base=16))
        await interaction.message.delete()
    if interaction.component.label == 'reroll':
        colorr = hex(random.randint(1118481,16777215))
        await interaction.respond(type=6)
        await interaction.message.edit(embed=discord.Embed(title='new color', description='click button below to confirm', color=int(colorr, base=16)), components=[Button(label='confirm', id=f'conf-{interaction.component.id.split("-")[1]}-{colorr}'), Button(label='cancel', id=f'canc-{interaction.component.id.split("-")[1]}'), Button(label='reroll', id=f'rero-{interaction.component.id.split("-")[1]}')])

@client.event
async def on_ready():
    await ready_status(client, config)
    pccs_feed.start()
    print("ready")
    global starttime
    starttime = time.time()
@client.command()
async def uptime(ctx):
    await ctx.send(f"The current uptime is: {str(datetime.timedelta(seconds=int(round(time.time()-starttime))))}")

@client.event
async def on_message(message):
    if message.author.bot: return
    await client.process_commands(message)

@client.command()
async def purge(ctx, limit=1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)

@tasks.loop(minutes=5)
async def pccs_feed():
    raw = xmltodict.parse(requests.get("https://www.pccsk12.com/Home/Components/RssFeeds/RssFeed/View?ctID=5&cateIDs=23").text)
    data = raw['rss']['channel']['item']
    if f"{data[0]['link']}" == f"{store('latest.json', 'message', True)}":
        return
    else:
        if data[0]['description'] == None: data[0]['description'] = 'No description provided'
        embed = discord.Embed(title=data[0]['title'], description=data[0]['description'], timestamp=datetime.datetime.utcnow(), color=discord.Color.blurple(), url=data[0]['link'])
        embed.set_footer(text='Retrieved')
        embed.set_author(name="P-CEP News post")
        # c = client.get_channel(886323743503298590)
        c = client.get_channel(886323743503298590)
        e = await c.send(content="<@&885280443044347915>", embed=embed)
        if c.type != discord.ChannelType.news:
            await c.send("Cannot publish to a non-news channel!")
        else:
            await e.publish()

        store('latest.json', 'message', val=data[0]['link'])


client.run(config['token'])
