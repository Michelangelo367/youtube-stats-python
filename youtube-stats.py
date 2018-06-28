import urllib.request as r
import json as j
from sys import argv
from colorama import init, Fore, Back

init() # only for windows 

key  = "<You API Key>" # this secret 
endpoint = "https://www.googleapis.com/youtube/v3/{}"

def colorize(string, color):
    return color + string + Fore.RESET

def humanize(number):
    number = int(number)
    name = ""
    if number > 10000:
        number = number / 1000
        name = "K"
        if number > 1000:
            number = number / 1000
            name = "M"
            if number > 1000:
                number = number / 1000
                name = "B"
    
    if not isinstance(number, int):
        return "{:.2f}{}".format(number, name)
    else:
        return "{:d}{}".format(number, name)

def printChannelStats(channelId, name):

    baseUrl = endpoint.format("channels") + "?part={}&id={}&key={}".format("statistics", channelId, key)
    request = r.Request(baseUrl)
    response = r.urlopen(request).read()

    result = j.loads(response)
    items = result['items'][0]
    statistics = items['statistics']
    subscriberCount = humanize(statistics['subscriberCount'])
    viewCount = humanize(statistics['viewCount'])
    videoCount = humanize(statistics['videoCount'])

    print("""{} has {} subscribers, {} views and has uploaded {} videos.""".format(colorize(name, Fore.RED), colorize(subscriberCount, Fore.GREEN), colorize(viewCount, Fore.BLUE), colorize(videoCount, Fore.MAGENTA)))

def searchforChannel(query):
    query = query.replace(" ", "+")
    baseUrl = endpoint.format("search") + "?part={}&q={}&key={}&type=channel".format("snippet", query, key)
    request = r.Request(baseUrl)
    response = r.urlopen(request).read()

    result = j.loads(response)
    items = result['items'][0]
    channelId = items['snippet']['channelId']
    name = items['snippet']['title']
    return { "channelId": channelId, "channelName": name }

if not len(argv) > 1:
    argv.append(input("YouTube Channel: "))
    
for index in range(1, len(argv)):
    channelDetails = searchforChannel(argv[index])
    printChannelStats(channelDetails['channelId'], channelDetails['channelName'])