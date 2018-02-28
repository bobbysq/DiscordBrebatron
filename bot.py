import discord
from discord.ext import commands
import configparser
from libbot import *
import random

config = configparser.ConfigParser()
config.read('config.ini')

DISCORD_TOKEN = config['DEFAULT']['DiscordToken']
TBA_APP_ID = config['DEFAULT']['TBAAppID']
TBA_AUTH_KEY = config['DEFAULT']['TBAAuthKey']
QUOTE_FILE = config['DEFAULT']['QuotesFile']
CURRENT_GAME = config['DEFAULT']['CurrentGame']
S_WORDS = ["stuff","spit","skit","ship","shirt","sport","short","script"] #TODO: put these into a CSV
MF_WORDS =["Monday-Friday","monkey-fightin","megaphonin","mighty flippin","Marty flyin","meadow frolickin","metal forgin"]

description = '''Brebatron is back in twon.'''
bot = commands.Bot(command_prefix='~', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=CURRENT_GAME))

@bot.command()
async def amlookup(productNo : int):
    """Looks up a part on AndyMark."""
    part = andymark_item(productNo)
    if part:
        #print(part)
        await bot.say("The item you looked up is a "+part[1]+". It costs "+part[2]+".")
    else:
        await bot.say("Item not found.")

@bot.command()
async def tba(teamNo : str):
    """Finds a team on The Blue Alliance"""
    teamName = tbaGetName(teamNo, TBA_APP_ID, TBA_AUTH_KEY)
    if teamName:
        await bot.say("TBA Link to team "+teamNo+", "+teamName+": https://thebluealliance.com/team/"+teamNo)
    else:
        await bot.say("TBA Link to team: https://thebluealliance.com/team/"+teamNo)

@bot.command()
async def quote():
    """Gets a quote from CD Spotlight"""
    quote = cdQuote()
    await bot.say(quote)

@bot.command()
async def robit():
    """Posts quotes from movie robots"""
    quote = movieQuote(QUOTE_FILE)
    await bot.say(quote)

@bot.command()
async def tsimfd():
    """When you guys leave here, and you go to your hometown..."""
    sWord = random.choice(S_WORDS)
    mfWord = random.choice(MF_WORDS)
    await bot.say("This "+sWord+" is "+mfWord+" dope. That's it.")

bot.run(DISCORD_TOKEN)
