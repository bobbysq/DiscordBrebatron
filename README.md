# Bobbysq's Discord bot

Uses:
* discord.py
* BeautifulSoup  

You can also install the lxml parser with `apt-get install python-lxml` if you want, but the program will use just Python's built in HTML parser if you don't have it.

I have added a requirements.txt so you can just cd to this repo, then run `pip install -r requirements.txt`

Before you run this bot, please change the config file options to change the TBA app ID to reflect your team number and set the MD5 hash of your name to be able to issue admin commands. You also need your Discord bot token.

Current Commands:
* !amlookup [part #]: Lookup a part on AndyMark
* ~~!about: Links back here~~
* !tba: looks up teams from thebluealliance.com
* !vexlookup [part #]: vex part lookup
* !tsimfd: Dispenses knowledge from the 2016 FIRST Championship
* !quote: Summons a quote from Chief Delphi
* !robit: Summons a quote from a famous movie robot
