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
   
#    async def on_raw_reaction_add(self, payload):
#        config = util.store('counterConfig.json', None, True) # none = no key, true = read
#        normChannel = config["countingNormalChannelID"]
#        seriousChannel = config["countingSeriousChannelID"]
#        roleID = config["countingRoleID"]
#        ownerIDs = store('config.json', 'owner_ids', True)
#        if (payload.emoji == "✅" or "☑️") and payload.user_id==510016054391734273 and payload.message.channel.id == normChannel:
#            countingDict = store("countingData.json", None, True)
#
#            if payload.message.user_id in countingDict.keys():
#               countingDict[payload.message.user_id] = countingDict[payload.message.user_id] + 1
#            else:
#                countingDict[payload.message.user_id] = 1
#            if countingDict[payload.message.user_id] == 100:
#                await payload.message.user_id.add_roles()

    async def on_message(self,message):
        config = util.store('counterConfig.json', None, True) # none = no key, true = read
        normChannel = config["countingNormalChannelID"]
        seriousChannel = config["countingSeriousChannelID"]
        roleID = config["countingRoleID"]
        emoji = config["emoji"]
        numbers=["1","2","3","4","5","6","7","8","9"]
        ownerIDs = store('config.json','owner_ids', True)
        WordList = message.content.split()
        number = True
        for i in WordList[0]:
            if i not in numbers:
                number = False
                break
        if message.channel.id == (normChannel or seriousChannel) and number == True:
            
            counterData = util.store('counterData.json',None, True)
            userDict = counterData.get(message.author.id, {"seriousCorrect":0,"seriousWrong":0,"normalCorrect":0,"normalWrong":0,"seriousFailures":[],"normalFailures":[],"normalScore":0,"seriousKicks":0,"seriousStreak":0})
            numSerious = counterData["numSerious"]
            numNormal = counterData["numNormal"]
            if message.channel.id == normChannel:
                if WordList[0] == (numNormal+1):
                    await message.add_reaction("✅")
                    util.addDict(userDict,"normalCorrect")
                    util.addDict(userDict,"normalScore")
                else:
                    await message.channel.send(f"{message.author} failed at {numNormal}! They've failed {userDict["normalWrong"]+1} times in this channel.")
                    util.addDict(userDict,"normalWrong")
                    util.addDict(userDict,"normalScore",-5)
            elif message.channel.id == seriousChannel:
                if WordList[0] == (numSerious+1):
                    await message.add_reaction("✅")
                    util.addDict(userDict,"seriousCorrect")
                else:
                    await message.channel.send(f"{message.author} failed at {numSerious}! They've failed {userDict["seriousWrong"]+1} times in this channel.")
                    util.addDict(userDict,"seriousWrong")
                    
                
        
        
        
        
        
                
def setup(bot):
    bot.add_cog(counter(bot))
