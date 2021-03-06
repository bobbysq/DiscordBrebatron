from bs4 import BeautifulSoup
import re
import urllib.request
import http
import json
import csv
import random

class andymark_item:
    def __init__(self, partnumber):
        self.url = 'http://www.andymark.com/product-p/am-'+ partnumber +'.htm'
        r = urllib.request.urlopen(self.url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
        try:
            soup = BeautifulSoup(r, "lxml")
        except:
            soup = BeautifulSoup(r, "html.parser")
        prices = soup.find_all("span", itemprop="price")
        if soup.title.get_text()=="AndyMark Robot Parts Kits Mecanum Omni Wheels":
            self.name = None
            self.price = None
        else:
            self.name = re.sub(r'\([^)]*\)', '', soup.title.get_text())
            #print(price[0].text)
            #money = price[0].text.encode('utf8','ignore')
            self.price = prices[0].get_text()

class vex_item:
    def __init__(self, partnumber):
        self.url = 'http://www.vexrobotics.com/'+str(partnumber)+'.html'
        r = urllib.request.urlopen(self.url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
        try:
            soup = BeautifulSoup(r, "lxml")
        except:
            soup = BeautifulSoup(r, "html.parser")
        prices = soup.find_all("span", class_="price")
        if soup.title.get_text()=="404: Page Not Found  - VEX Robotics":
            self.name = None
            self.price = None
        else:
            self.name = re.sub(r'\([^)]*\)', '', soup.title.get_text())
            self.price = prices[0].get_text()

def tbaGetName(team, appid, auth):
    try:
        url = "/api/v3/team/frc"+str(team)
        keys = {"X-TBA-Auth-Key" : auth, "X-TBA-App-Id" : appid}
        print(url)
        c = http.client.HTTPSConnection("www.thebluealliance.com")
        c.request("GET", url, headers = keys)
        response = c.getresponse()
        teamData = response.read().decode("utf-8")
        #print(teamData)
        data = json.loads(teamData)
        return data['nickname']
    except:
        return(None)

def cdQuote(): #Remember CDValentinesScraper? Well it's back, in chatbot form!
    try:
        url = 'https://www.chiefdelphi.com/forums/portal.php'
        r = urllib.request.urlopen(url).read()
        try:
            soup = BeautifulSoup(r, "lxml")
        except:
            soup = BeautifulSoup(r, "html.parser")
        quote = soup.find("td", class_="spotlight").contents

        cleanedQuote=quote[1]
        author = quote[2].get_text()
        return(cleanedQuote+author)
    except:
        return(None)

def movieQuote(quotesFile):
    csvfile = open(quotesFile, newline='')
    quotereader = csv.reader(csvfile, dialect='excel')
    quotedata = list(quotereader)
    entry  = quotedata[random.randint(1,len(quotedata)-1)] #len() counts from 1
    author = entry[0]
    source = entry[1]
    quote  = entry[random.randint(2,6)]
    return(quote + " - " + author + ", " + source)

def reminder():
    #TODO: AUTOMATE THIS
    print("this thing doesn't even work yet, why are you calling it")
