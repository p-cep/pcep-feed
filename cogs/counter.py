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
            userDict = counterData.get(message.author.id, {"seriousCorrect":0,"seriousWrong":0,"normalCorrect":0,"normalWrong":0,"seriousFailures":[],"normalFailures":[],"normalScore":0,"seriousStreak":0,"normalStreak":0})
            numSerious = counterData["numSerious"]
            numNormal = counterData["numNormal"]
            if message.channel.id == normChannel:
                if WordList[0] == (numNormal+1):
                    await message.add_reaction("✅")
                    util.addDict(userDict,"normalCorrect")
                    if userDict["normalScore"] != -1:
                        util.addDict(userDict,"normalScore")
                else:
                    util.addDict(userDict,"normalWrong")
                    await message.add_reaction("❌")
                    await message.channel.send(f"{message.author} failed at {numNormal}! They've failed {userDict["normalWrong"]} times in this channel.")
                    
                    if userDict["normalScore"] != -1:
                        util.addDict(userDict,"normalScore",-5)
                    userDict["normalFailures"].append(numNormal)
                    numNormal=0
            elif message.channel.id == seriousChannel:
                if WordList[0] == (numSerious+1):
                    await message.add_reaction("✅")
                    util.addDict(userDict,"seriousCorrect")
                else:
                    util.addDict(userDict,"seriousWrong")
                    await message.add_reaction("❌")
                    
                    ending = "th"
                    if userDict["seriousWrong"] == 1:
                        ending = "st"
                    elif userDict["seriousWrong"] == 2:
                        ending = "nd"
                    elif  userDict["seriousWrong"] == 3:
                        ending="st"
                    await message.channel.send(f"{message.author.mention} failed at {numSerious}, the correct number was {numSerious+1}! They are getting kicked from the serious channel for the {userDict[seriousWrong]}{ending} time.")
                    userDict["normalScore"] = 0
                    
                    userDict["seriousFaliures"].append(numSerious)
                    numSerious=0
                    
                    
                    
                
        
        
        
        
        
                
def setup(bot):
    bot.add_cog(counter(bot))
