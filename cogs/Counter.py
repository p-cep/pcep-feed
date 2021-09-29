import asyncio
import discord
from discord.ext import commands
from cogs import util

class Counter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        config = util.store('counterConfig.json', None, True) # none = no key, true = read
        normChannel = config["countingNormalChannelID"]
        seriousChannel = config["countingSeriousChannelID"]
        roleID = config["countingRoleID"]
        ownerIDs = store('config.json', 'owner_ids', True)
        if (payload.emoji == "✅" or "☑️") and payload.user_id==510016054391734273 and payload.message.channel.id == normChannel:
            countingDict = store("countingData.json", None, True)

            if payload.message.user_id in countingDict.keys():
                countingDict[payload.message.user_id] = countingDict[payload.message.user_id] + 1
            else:
                countingDict[payload.message.user_id] = 1
            if countingDict[payload.message.user_id] == 100:
                await payload.message.user_id.add_roles()
                
def setup(bot):
    bot.add_cog(Counter(bot))
