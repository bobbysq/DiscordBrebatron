from bs4 import BeautifulSoup
import re
import urllib.request
import http
import json
import csv
import random

class andymark_item:
    def __init__(self, partnumber):
        self.url = 'http://www.andymark.com/am-'+ partnumber
        try:
            r = urllib.request.urlopen(self.url).read() #TODO: Change this to use http.client so we don't have 2 libraries doing the same thing
            try:
                soup = BeautifulSoup(r, "lxml")
            except:
                soup = BeautifulSoup(r, "html.parser")
            prices = soup.find_all("meta", {"itemprop" : "price"}) #get all prices on the page
            #title = re.sub(r'\([^)]*\)', '', soup.title.get_text()).strip()
            self.name = soup.title.get_text().strip()[:-16]
            #print(price[0].text)
            #money = price[0].text.encode('utf8','ignore')
            self.price = float(prices[0]["content"]) #just get the price we want
        except:
            self.name = None
            self.price = None

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
            self.name = re.sub(r'\([^)]*\)', '', soup.title.get_text())[:-15]
            self.price = prices[0].get_text()

class weatherLookup:
    def __init__(self, apiKey, zip, country):
        weatherStr = ""
        url = "/data/2.5/weather?zip="+ str(zip) + ","+ country + "&APPID="+apiKey
        print(url)
        c = http.client.HTTPSConnection("api.openweathermap.org")
        c.request("GET", url)
        response = c.getresponse()
        weatherData = response.read().decode("utf-8")
        #print(teamData)
        data = json.loads(weatherData)
        if country == "us":
            temp = str(round(float(data['main']['temp']) * (9/5) - 459.67, 2)) + " F"
        else:
            temp = str(round(float(data['main']['temp']) - 273.15, 2)) + " C"
        self.city = data['name']
        for weathers in data['weather']:
            weatherStr = weatherStr + ", " + weathers['description']
        weatherStr = weatherStr[2:] # Remove the beginning ", "
        self.weather = weatherStr
        #self.weather = "test"
        self.temperature = temp

class cdQuote: #Remember CDValentinesScraper? Well it's back, in chatbot form!
    def __init__(self):
        try:
            url = 'https://www.chiefdelphi.com/forums/portal.php'
            r = urllib.request.urlopen(url).read()
            try:
                soup = BeautifulSoup(r, "lxml")
            except:
                soup = BeautifulSoup(r, "html.parser")
            quote = soup.find("td", class_="spotlight").contents

            self.quote = quote[1]
            self.author = quote[2].get_text()
        except:
            self.quote = None
            self.author = None


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

def ruleLookup(ruleNo, manualFile):
    try:
        with open(manualFile,'r') as f:
            try:
                soup = BeautifulSoup(f, "lxml")
            except:
                soup = BeautifulSoup(f, "html.parser")
        rule = soup.find_all("a", attrs = {"name" : ruleNo}) #find an <a> tag with the rule number
        ruleTexts = rule[0].parent.strings
        endMsg = ""
        for text in ruleTexts: #some rules come in chunks, so .string doesn't quite work
            #print(text.encode("utf-8"))
            endMsg = endMsg + text.replace("\n", " ") #delete any stray newlines
        return(endMsg)
    except:
        return(None)

# def cdQuote(): #Remember CDValentinesScraper? Well it's back, in chatbot form!
#     try:
#         url = 'https://www.chiefdelphi.com/forums/portal.php'
#         r = urllib.request.urlopen(url).read()
#         try:
#             soup = BeautifulSoup(r, "lxml")
#         except:
#             soup = BeautifulSoup(r, "html.parser")
#         quote = soup.find("td", class_="spotlight").contents

#         cleanedQuote=quote[1]
#         author = quote[2].get_text()
#         return(cleanedQuote+author)
#     except:
#         return(None)

def movieQuote(quotesFile):
    csvfile = open(quotesFile, newline='')
    quotereader = csv.reader(csvfile, dialect='excel')
    quotedata = list(quotereader)
    entry  = quotedata[random.randint(1,len(quotedata)-1)] #len() counts from 1
    author = entry[0]
    source = entry[1]
    quote  = entry[random.randint(2,6)]
    return(quote + " - " + author + ", " + source)

