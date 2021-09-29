import discord
from discord.ext import commands
from discord.ext.commands.core import command
from cogs import util
import asyncio
import json

class Counter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with open ("../config.json","r") as config:
            normChannel = config["countingNormalChannelID"]
            seriousChannel = config["countingSeriousChannelID"]
            roleID = config["countingRoleID"]
            ownerIDs = config["owner_ids"]
        if (payload.emoji.name == "white_check_mark" or "ballot_box_with_check") and payload.user_id==510016054391734273 and payload.message.channel.id == normChannel:
            with open ("../countingData.json","r") as file:
                countingDict = json.load(file)

            if payload.message.user_id in countingDict.keys():
                countingDict[payload.message.user_id] = countingDict[payload.message.user_id] + 1
            else:
                countingDict[payload.message.user_id] = 1
            if countingDict[payload.message.user_id] == 100:
                await payload.message.user_id.add_roles()
                
