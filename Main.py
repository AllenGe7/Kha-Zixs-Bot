import discord
import requests
import urllib.request, json
import urllib3
import string
urllib3.disable_warnings()
from collections import defaultdict
import operator
from ast import literal_eval
import urllib
from PIL import Image
import shutil

client = discord.Client()


@client.event
async def on_ready():
    print(f"We are logged in as {client.user}")

@client.event
async def on_message(message):  # event that happens per any message.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if "!counter" in message.content:
        champion = message.content.replace("!counter ", "").split()[0]

        position = message.content.replace("!counter ", "").split()[1]
        output = getChampion(userErrorChampion(champion), userErrorPosition(position))
        for x in output:
            await client.send_message(message.channel, x, tts=True)
    if "!popular" in message.content:
        champion = message.content.replace("!popular ", "").split()[0]
        position = message.content.replace("!popular ", "").split()[1]
        await client.send_message(message.channel, popularBuild(champion, position), tts=True)

        printBuild(popularBuild(userErrorChampion(champion), userErrorPosition(position)))
        with open('pasted_image.png', 'rb') as f:
            await client.send_file(message.channel, f)
    if "!winning" in message.content:
        champion = message.content.replace("!winning ", "").split()[0]
        position = message.content.replace("!winning ", "").split()[1]
        await client.send_message(message.channel, popularBuild(champion, position), tts=True)

        printBuild(winnestBuild(userErrorChampion(champion), userErrorPosition(position)))
        with open('pasted_image.png', 'rb') as f:
            await client.send_file(message.channel, f)
    if "!help" in message.content:
        await client.send_message(message.channel, "!popular, !winning, !counter")

def getChampion(input, role):
    url = 'http://api.champion.gg/champion/' + input + '/matchup?api_key=d143ded682d41d1e3ebe173d0b327e46'
    response = requests.get(url, verify=True)
    data = response.json();
    result = []

    for item in data:
        if (item.get('role') == role):
            for x in item.get("matchups"):
                result.append(x)
    print(result)
    # sorted_d = sorted(result.items(), key=operator.itemgetter(0))
    win = 0;
    resultPrint = []
    for x in sorted(result, key=lambda i: (i['winRate'], i['games']), reverse=True):
        if (x.get('winRate') > 50):
            str = x.get('key'), x.get('winRate'), x.get('games')
            resultPrint.append(str)
    return resultPrint

def userErrorChampion(str):
    str.lower()
    str[0].upper()
    table = str.maketrans(dict.fromkeys(string.punctuation))
    str = str.translate(table)
    print(str)
    return str;

def userErrorPosition(str):
    if (str == "Mid"):
        return "Middle"
    if (str == "adc"):
        return "ADC"
    str.lower()
    str[0].upper()
    return str

#urllib.urlretrieve("http://ddragon.leagueoflegends.com/cdn/5.1.2/img/item/3128.png", "00000001.jpg")
def popularBuild(champion, position):
    #http: // api.champion.gg / champion / annie / items / finished / mostPopular?api_key = d143ded682d41d1e3ebe173d0b327e46
    url = 'http://api.champion.gg/champion/' + champion + '/items/finished/mostPopular?api_key=d143ded682d41d1e3ebe173d0b327e46'
    response = requests.get(url, verify=True)
    data = response.json();
    result = []
    for item in data:
        if item.get('role') == position:
            result.append(item.get('items'))
    flat_list = [item for sublist in result for item in sublist]
    for image in flat_list:
        url = 'http://ddragon.leagueoflegends.com/cdn/8.2.1/img/item/' + str(image) + '.png'
        url_response = requests.get(url, stream=True)
        with open( str(image) + '.png', 'wb') as out_file:
            shutil.copyfileobj(url_response.raw, out_file)
        del url_response
    return flat_list
def winnestBuild(champion, position):
    url = 'http://api.champion.gg/champion/' + champion + '/items/finished/mostWins?api_key=d143ded682d41d1e3ebe173d0b327e46'
    response = requests.get(url, verify=True)
    data = response.json();
    result = []
    for item in data:
        if item.get('role') == position:
            result.append(item.get('items'))
    flat_list = [item for sublist in result for item in sublist]
    for image in flat_list:
        url = 'http://ddragon.leagueoflegends.com/cdn/8.2.1/img/item/' + str(image) + '.png'
        url_response = requests.get(url, stream=True)
        with open(str(image) + '.png', 'wb') as out_file:
            shutil.copyfileobj(url_response.raw, out_file)
        del url_response
    return flat_list
def printBuild(itemList):
    image = Image.open("test.png")
    new_image = image.resize((384, 64))
    index = 0
    for x in itemList:
        print(x)
        logo = Image.open(str(x) + '.png')
        image_copy = new_image.copy()
        position = (index, 0)
        image_copy.paste(logo, position)
        image_copy.save('pasted_image.png')
        index += 64
        new_image = image_copy
    image_copy.show()

client.run("NTA0Nzg4NjA3NDQyMjIzMTM0.DrKZBw.gYtkzt_4qFZDOf2Id1OQ_5th3dk")
