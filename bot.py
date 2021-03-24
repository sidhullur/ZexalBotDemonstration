import discord
import time
from discord.ext import commands
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
import random
import requests
import asyncio

queue = {}
dictionary = PyDictionary()
looping = {}

PUBLIC_KEY = "<MyPublicKey>"
SECRET_KEY = "<MySecretKey>"
auth = requests.auth.HTTPBasicAuth(PUBLIC_KEY, SECRET_KEY)
sync = asyncio.get_event_loop()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
whitelisted_channels = []

data = {
    'grant_type' : 'password',
    'username' : '<MyUsername>',
    'password' : '<MyPassword>'
}

token = "<MyToken>"
client = commands.Bot(command_prefix = commands.when_mentioned_or('zx '))
client.remove_command('help')

@client.event
async def on_ready():
    print("Online")
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="zx | @Zexal"))

async def check_whitelist(channel):
    if channel.id in whitelisted_channels:
        await channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("Hello! I am Zexal and I currently serve the server you just joined.")
    await member.dm_channel.send("My command prefix is 'zx'. Use 'zx help' in the server to get a list of commands.")
    await member.dm_channel.send("Welcome and enjoy your stay!")

@client.command()
async def version(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    embed = discord.Embed(title="Zexal Bot, Version 3.2", color=discord.Colour.from_rgb(102, 25 ,255))
    embed.add_field(name="Changelog:", value="Fixed major issues with queuing in multiple guilds.", inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def time(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    hour = time.localtime().tm_hour
    min = time.localtime().tm_min
    ampm = "AM"
    if hour < 7:
        day = days[time.localtime().tm_wday - 1]
    else:
        day = days[time.localtime().tm_wday]

    hour = time.localtime().tm_hour-7
    if hour < 0:
        hour = 24 + hour

    if (hour > 12):
        hour -= 12
        ampm = "PM"
    if min < 10:
        min = "0" + str(min)
    else:
        min = str(min)
    await ctx.channel.send(str(hour) + ":" + min + " " + ampm + ", " + day)

@client.command()
async def help(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    embed = discord.Embed(title="Commands", description="List of commands Zexal can use.", color=discord.Colour.from_rgb(102, 25 ,255)
                          , url="https://youtu.be/4KciJwOF3oM?t=1")
    embed.set_thumbnail(url="https://pbs.twimg.com/media/EEUuiYuU8AAOmzE.jpg")
    embed.add_field(name="version", value = "Returns the version and changelog of Zexal.", inline=True)
    embed.add_field(name="time", value="Returns the local time.", inline=True)
    embed.add_field(name="weather (place) ", value="Returns a link to the weather in a City or State.", inline=True)
    embed.add_field(name="link", value="Returns a link to add Zexal to a server.", inline=True)
    embed.add_field(name="suggest (suggestion)", value="Zexal will take suggestions of new features or fixes.", inline=True)
    embed.add_field(name="delete (number of messages)", value="Zexal will delete the last messages by the number. \n Only accessible by admins.", inline=True)
    embed.add_field(name="announce (announcement)", value="Zexal will send an embedded announcement. Mentions everyone.", inline=True)
    embed.add_field(name="whitelist", value="Zexal will whitelist the channel, preventing command responses.", inline=True)
    embed.add_field(name="define (word)", value="Zexal will return all definitions of the given word.", inline=True)
    embed.add_field(name="search (phrase)", value="Zexal will search for and return images related to the phrase.", inline=True)
    embed.add_field(name="meme", value="Zexal will return a meme from r/memes", inline=True)
    embed.add_field(name="dankmeme", value="Zexal will return a meme from r/dankmemes", inline=True)
    embed.add_field(name="help", value="Returns a list of commands Zexal responds to.", inline=True)
    await ctx.channel.send(embed=embed)

@client.command()
async def weather(ctx, *, city):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    #try:
    query = ""
    for num,i in enumerate(city):
        if i == " ":
            query += ("+")
            continue
        query += i
    try:
        url = f"https://www.google.com/search?q=weather+in+{query}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        weather = soup.find_all("div", {"class": "BNeawe"})
        temp = weather[1].text
        status = weather[2].text
    except:
        await ctx.channel.send("Sorry! That isn't a valid location.")
        return
    if not "°F" in temp:
        await ctx.channel.send("Sorry! That isn't a valid location.")
        return


    phrase = 'https://youtu.be/Pa67b28h0vY'
    embed = discord.Embed(title=("Weather"), url = phrase, color=discord.Colour.from_rgb(102, 25 ,255))
    embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/81%2BeUvsHXoL.png")
    embed.add_field(name="Temperature", value=f"{temp}", inline=False)
    embed.add_field(name="Location", value=f"{city}", inline=False)
    embed.add_field(name="Status", value=f"{status}", inline=False)
    embed.add_field(name="URL", value=f"{url}")
    await ctx.send(embed=embed)
    #except:
       # await ctx.channel.send("Sorry that is incorrect syntax.")

@client.command()
async def link(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    embed = discord.Embed(title="Invite Zexal Bot", color=discord.Colour.from_rgb(102, 25 ,255), url="https://discord.com/api/oauth2/authorize?client_id=805907366016057354&permissions=8&scope=bot",)
    await ctx.channel.send(embed=embed)

@client.command()
async def suggest(ctx, *, str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    user = ctx.message.author
    await ctx.message.delete()
    channel = discord.Client.get_channel(client, 807288531164201032)
    await channel.send(f"New Suggestion by {user.name}: " + str)
    await ctx.channel.send("Your suggestion has been noted. Thank you.")

@client.command()
async def delete(ctx, num):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    if (not ctx.message.author.guild_permissions.administrator):
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        return
    try:
        num = int(num)
    except:
        await ctx.channel.send("The parameter should be an integer.")
        return

    await ctx.channel.purge(limit=num+1)

@client.command()
async def announce(ctx, *, str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    if (not ctx.message.author.guild_permissions.administrator):
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        return
    await ctx.message.delete()
    await ctx.channel.send(ctx.guild.default_role)
    embed = discord.Embed(title=(str), color=discord.Colour.from_rgb(102, 25 ,255))
    await ctx.channel.send(embed=embed)

@client.command()
async def whitelist(ctx):
    if (not ctx.message.author.guild_permissions.administrator):
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        return
    if ctx.channel.id in whitelisted_channels:
        whitelisted_channels.remove(ctx.channel.id)
        await ctx.channel.send("This channel has been un-whitelisted.")
        return
    whitelisted_channels.append(ctx.channel.id)
    await ctx.channel.send("This channel has been whitelisted.")

@client.command()
async def define(ctx, *, word):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    embed = discord.Embed(title=f"Definitions of {word}", url = "https://youtu.be/zqflC-as2Qo", color=discord.Colour.from_rgb(102, 25 ,255))
    meanings = dictionary.meaning(word)
    if meanings == None:
        await ctx.channel.send(f"Sorry, I couldn't find any results for '{word}'.")
        await ctx.channel.send("Please make sure you spelled the word correctly.")
        return
    for i in list(meanings.keys()):
        string = ""
        for z in meanings[i]:
            string = string + " " + z + "\n\n"
        embed.add_field(name=i, value=string, inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def search(ctx, *,query):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    res = requests.get("https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch")
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all("img")[1:4]
    for i in results:
        await ctx.channel.send(i["src"])

@client.command()
async def meme(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

    res = requests.get('https://oauth.reddit.com/r/memes/hot', headers=headers)
    URLs = []
    captions = []
    for post in res.json()['data']['children']:
        url = post['data']['url_overridden_by_dest']
        if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".gif"):
            URLs.append(url)
            captions.append(post['data']['title'])

    num = random.randint(0, len(URLs) - 1)
    embed = discord.Embed(title=captions[num], url= "https://www.reddit.com/r/memes/",color=discord.Colour.from_rgb(102, 25 ,255))
    embed.set_image(url=URLs[num])
    embed.set_footer(text="All memes from r/memes.")
    await ctx.channel.send(embed=embed)

@client.command()
async def dankmeme(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

    res = requests.get('https://oauth.reddit.com/r/dankmemes/hot', headers=headers)
    URLs = []
    captions = []
    for post in res.json()['data']['children']:
        url = post['data']['url_overridden_by_dest']
        if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".gif"):
            URLs.append(url)
            captions.append(post['data']['title'])

    num = random.randint(0, len(URLs) - 1)
    embed = discord.Embed(title=captions[num], url="https://www.reddit.com/r/memes/",
                          color=discord.Colour.from_rgb(102, 25, 255))
    embed.set_image(url=URLs[num])
    embed.set_footer(text="All memes from r/dankmemes.")
    await ctx.channel.send(embed=embed)

@client.command()
async def error(ctx, *, str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    user = ctx.message.author
    await ctx.message.delete()
    channel = discord.Client.get_channel(client, 822919446585802752)
    await channel.send(f"Error logged by {user.name}: " + str)
    await ctx.channel.send("Your error has been logged. Thank you.")

client.run(token)
