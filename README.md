# Bobbysq's Discord bot

Uses:

* discord.py
* BeautifulSoup  

You can also install the lxml parser with `apt-get install python-lxml` if you want, but the program will use just Python's built in HTML parser if you don't have it.

I have added a requirements.txt so you can just cd to this repo, then run `pip install -r requirements.txt`. You'll also need to download the HTML file of the current FRC rule manual. You can find it [here](https://firstfrc.blob.core.windows.net/frc2019/Manual/HTML/2019FRCGameSeasonManual.htm).

Before you run this bot, please change the config file options to change the TBA app ID to reflect your team number. You also need your Discord bot token and OpenWeatherMap API Key.

Current Commands:

* ~amlookup [part #]: Lookup a part on AndyMark
* ~source: Links back here
* ~tba: looks up teams from thebluealliance.com
* ~vexlookup [part #]: vex part lookup
* ~tsimfd: Dispenses knowledge from the 2016 FIRST Championship
* ~quote: Summons a quote from Chief Delphi
* ~robit: Summons a quote from a famous movie robot
* ~hug : Hugs a user
* ~weather: Looks up the weather in an area
