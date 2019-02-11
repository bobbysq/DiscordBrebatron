import discord
from discord.ext import commands
import configparser
import libbot
import random

config = configparser.ConfigParser()
config.read('config.ini')

DISCORD_TOKEN = config['DEFAULT']['DiscordToken']
TBA_APP_ID = config['DEFAULT']['TBAAppID']
TBA_AUTH_KEY = config['DEFAULT']['TBAAuthKey']
QUOTE_FILE = config['DEFAULT']['QuotesFile']
CURRENT_GAME = config['DEFAULT']['CurrentGame']
WEATHER_KEY = config['DEFAULT']['WeatherID']
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

@bot.command(pass_context=True)
async def amlookup(ctx, productNo : str):
    """Looks up a part on AndyMark."""
    bot.send_typing(ctx.message.channel)
    part = libbot.andymark_item(productNo)
    if part.name:
        #print(part)
        msg = discord.Embed(title="AndyMark Product", url = part.url, color = 0x273895)
        #msg.set_thumbnail(url="http://cdn3.volusion.com/vyfsn.knvgw/v/vspfiles/photos/am-" + productNo + "-1.jpg")
        msg.add_field(name="Name",value=part.name)
        formattedPrice = "$" + "{0:.2f}".format(part.price)
        msg.add_field(name="Price", value = formattedPrice)
        await bot.say(embed=msg)
        # await bot.say("The item you looked up is a "+part.name+". It costs "+part.price+".")
    else:
        await bot.say("Item not found.")

@bot.command(pass_context=True)
async def vexlookup(ctx, productNo : str):
    """Looks up a part on VEX Robotics."""
    bot.send_typing(ctx.message.channel)
    part = libbot.vex_item(productNo)
    if part.name:
        #print(part)
        msg = discord.Embed(title="VEX Product", url = part.url, color = 0x009639)
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
    teamName = libbot.tbaGetName(teamNo, TBA_APP_ID, TBA_AUTH_KEY)
    if teamName:
        msg = discord.Embed(title=teamName, url =  "https://thebluealliance.com/team/"+teamNo, color = 0x0000ff)
        msg.add_field(name="Name",value=teamName)
        msg.add_field(name="Number",value=teamNo)
        await bot.say(embed=msg)
    else:
        await bot.say("TBA Link to team: https://thebluealliance.com/team/"+teamNo)

# @bot.command() #Depricated until Brandon uploads the Spotlight backup
# async def quote():
#     """Gets a quote from CD Spotlight"""
#     quote = libbot.cdQuote()
#     msg = discord.Embed(title="Chief Delphi Quote", color = 0xff8800)
#     print(quote.quote)
#     print(quote.author)
#     msg.add_field(name=quote.quote[:-2], value=quote.author)
#     print(msg)
#     await bot.say(embed=msg)

@bot.command()
async def robit():
    """Posts quotes from movie robots"""
    quote = libbot.movieQuote(QUOTE_FILE)
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

@bot.command() #shoutouts to arynbot
async def hug(member : discord.Member):
    """Hugs a member."""
    await bot.say('*hugs {0.name}*'.format(member))

@bot.command() #suggested by hook
async def weather(zipCode : str, country = "us"):
    """Looks up the weather of a zip code."""
    weatherIn = libbot.weatherLookup(WEATHER_KEY, zipCode, country)
    msg = discord.Embed(title="Weather in " + weatherIn.city)
    msg.add_field(name="City",value=weatherIn.city)
    msg.add_field(name="Weather",value=weatherIn.weather)
    msg.add_field(name="Temperature",value=weatherIn.temperature)
    await bot.say(embed=msg)

@bot.command()
async def manual(ruleNo = ""):
    """Looks up a rule in the game manual"""
    url = "https://firstfrc.blob.core.windows.net/frc2019/Manual/HTML/2019FRCGameSeasonManual.htm#" + ruleNo
    await bot.say(url)


@bot.command()
async def source():
    """Links the source code"""
    await bot.say("Source code located at https://gitlab.com/bobbysq/DiscordBrebatron")

bot.run(DISCORD_TOKEN)
