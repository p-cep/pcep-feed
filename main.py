import discord
import requests
import xmltodict
import datetime
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from cogs.util import store, ready_status

config = store('config.json', None, True)
client = commands.Bot(command_prefix=config['pfx'], help_command=None, owner_ids=config['owner_ids'])
slash = SlashCommand(client, sync_commands=True, debug_guild=885634787119886337)

@slash.slash(name='join', description='Get an invite to the P-CEP discord')
async def _join(ctx):
    await ctx.send("https://discord.gg/rHYsNSbxG7", hidden=True)

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
    if f"{client.user.id}" in message.content and 'can i go on a date' not in message.content:
        await message.reply(content="what the fuck do you want bitch")
    elif f"{client.user.id}" in message.content and 'can i go on a date' in message.content:
        if message.author.id not in config['owner_ids']:
            await message.reply(content="srry i have boyfriend")
            return
        await message.reply(content="yes bb ofc i will go on date w/ u :kissing_heart:")
    await client.process_commands(message)

@client.command()
@commands.is_owner()
async def test(ctx):
    await pccs_feed()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def start(ctx):
    pccs_feed.start()
    await ctx.send("started task loop")

@client.command()
@commands.is_owner()
async def stop(ctx):
    pccs_feed.stop()
    await ctx.send("Stopped the task loop. Please note you must start it up again with `p/start`")

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
        c = client.get_channel(886323743503298590)
        e = await c.send(content="<@&885280443044347915>", embed=embed)
        await e.publish()
        store('latest.json', 'message', val=data[0]['link'])


client.run(config['token'])
