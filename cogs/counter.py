import asyncio
import discord
from discord.ext import commands
from cogs import util as *
import json

class counter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    #Code that was assuming that I had to check whether or not the counting bot reacted, but I don't so its fine
    """
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
"""
    async def on_message(self,message):
        config = store('counterConfig.json', None, True) # none = no key, true = read
        normChannel = config["countingNormalChannelID"]
        seriousChannel = config["countingSeriousChannelID"]
        roleID = config["countingRoleID"]
        ownerIDs = store('config.json','owner_ids', True)
        counterData = store('counterData.json',None, True)
        userDict = counterData.get(message.author.id, False)
        numSerious = counterData["numSerious"]
        
        
                
def setup(bot):
    bot.add_cog(counter(bot))
