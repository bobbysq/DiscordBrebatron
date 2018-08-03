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

random.seed()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Add bot at:")
    print("https://discordapp.com/oauth2/authorize?&client_id=" + \
    bot.user.id + "&scope=bot&permissions=0")
    print('------')
    await bot.change_presence(game=discord.Game(name=CURRENT_GAME))

@bot.command()
async def amlookup(productNo : str):
    """Looks up a part on AndyMark."""
    part = andymark_item(productNo)
    if part.name:
        #print(part)
        msg = discord.Embed(title="AndyMark Product", url = part.url, color = 0x0000ff)
        msg.set_thumbnail(url="http://cdn3.volusion.com/vyfsn.knvgw/v/vspfiles/photos/am-" + productNo + "-1.jpg")
        msg.add_field(name="Name",value=part.name)
        msg.add_field(name="Price",value=part.price)
        await bot.say(embed=msg)
        # await bot.say("The item you looked up is a "+part.name+". It costs "+part.price+".")
    else:
        await bot.say("Item not found.")

@bot.command()
async def vexlookup(productNo : str):
    """Looks up a part on VEX Robotics."""
    part = vex_item(productNo)
    if part.name:
        #print(part)
        msg = discord.Embed(title="VEX Product", url = part.url, color = 0x00ff00)
        thumbUrl="https://www.vexrobotics.com/media/catalog/product/cache/1/" +\
        "small_image/300x/17f82f742ffe127f42dca9de82fb58b1/2/1/" + productNo + ".jpg"
        msg.set_thumbnail(url=thumbUrl)
        msg.add_field(name="Name",value=part.name)
        msg.add_field(name="Price",value=part.price)
        await bot.say(embed=msg)
        # await bot.say("The item you looked up is a "+part.name+". It costs "+part.price+".")
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

@bot.command()
async def rng(sides : int):
    """Generates a random number"""
    if (sides >= 1):
        number = random.randint(1,sides)
        await bot.say(number)
    else:
        await bot.say("How am I supposed to roll a "+ str(sides) +" sided die?")

bot.run(DISCORD_TOKEN)
