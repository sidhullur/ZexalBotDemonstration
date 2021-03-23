import discord
import youtube_dl
import time
from discord.ext import commands
from bs4 import BeautifulSoup
import random
import requests
import asyncio

queue = {}
looping = {}

PUBLIC_KEY = "<MyPublicKey>"
SECRET_KEY = "<MySecretKey>"
auth = requests.auth.HTTPBasicAuth(PUBLIC_KEY, SECRET_KEY)
loop = asyncio.get_event_loop()
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

def check_whitelist(channel):
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

@client.command(aliases=["time"])
async def current_time(ctx):
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
        hour = 12 + hour

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
    embed.add_field(name="join", value="Zexal joins the VC the Client is currently in.", inline=True)
    embed.add_field(name="leave", value="Zexal leaves the VC the Client is currently in.", inline=True)
    embed.add_field(name="suggest (suggestion)", value="Zexal will take suggestions of new features or fixes.", inline=True)
    embed.add_field(name="play (url or audio name)", value="Zexal will stream Youtube audio in VC.", inline=True)
    embed.add_field(name="pause", value="If audio is playing, Zexal will pause it.", inline=True)
    embed.add_field(name="resume", value="If audio is paused, zexal will resume playback.", inline=True)
    embed.add_field(name="stop", value="Zexal will stop the currently playing audio and clear the queue.", inline=True)
    embed.add_field(name="q", value="Zexal will display the current queue.", inline=True)
    embed.add_field(name="skip", value="Zexal will skip the current song.", inline=True)
    embed.add_field(name="delete (number of messages)", value="Zexal will delete the last messages by the number. \n Only accessible by admins.", inline=True)
    embed.add_field(name="announce (announcement)", value="Zexal will send an embedded announcement. Mentions everyone.", inline=True)
    embed.add_field(name="whitelist", value="Zexal will whitelist the channel, preventing command responses.", inline=True)
    embed.add_field(name="define (word)", value="Zexal will return all definitions of the given word.", inline=True)
    embed.add_field(name="search (phrase)", value="Zexal will search for and return images related to the phrase.", inline=True)
    embed.add_field(name="meme", value="Zexal will return a meme from r/memes", inline=True)
    embed.add_field(name="dankmeme", value="Zexal will return a meme from r/dankmemes", inline=True)
    embed.add_field(name="echo (phrase)", value="Zexal will restate a given phrase.", inline=True)
    embed.add_field(name="loop", value="Zexal will loop or unloop the queue.", inline=True)
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
async def join(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    if(ctx.author.voice != None):
        if ctx.voice_client != None:
            await ctx.voice_client.disconnect()
        channel = ctx.author.voice.channel
        await ctx.message.add_reaction("👍")
        await channel.connect()
    else:
        await ctx.channel.send("Please join a voice channel before using that command.")

@client.command()
async def leave(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if(ctx.voice_client != None):
        if voice.is_playing():
            voice.stop()
        queue.clear()
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction("👋")
    else:
        await ctx.channel.send("I am not currently in a voice channel.")

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
async def play(ctx, *, url : str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return

    global queue
    global looping
    global loop
    if(not ctx.guild.id in queue):
        queue[ctx.guild.id] = []
    if(not ctx.guild.id in looping):
        looping[ctx.guild.id] = False

    def remove_song():
        if len(queue[ctx.guild.id]) > 0:
            queue[ctx.guild.id].pop(0)
        loop.create_task(check_queue())

    def looper():
        if len(queue[ctx.guild.id])==0:
            return
        song = queue[ctx.guild.id].pop(0)
        queue[ctx.guild.id].append(song)
        loop.create_task(check_queue())

    async def check_queue():
        if len(queue[ctx.guild.id]) == 0:
            return
        embed = discord.Embed(title=f"Now Playing: {queue[ctx.guild.id][0]['entries'][0]['title']}.", url=queue[ctx.guild.id][0]["entries"][0]["webpage_url"], color=discord.Colour.from_rgb(102, 25, 255))
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        await ctx.channel.send(embed=embed)
        if looping[ctx.guild.id]==False:
            voice.play(discord.FFmpegPCMAudio(queue[ctx.guild.id][0]["entries"][0]["formats"][0]["url"], **FFMPEG_OPTS), after=lambda e: remove_song())
        else:
            voice.play(discord.FFmpegPCMAudio(queue[ctx.guild.id][0]["entries"][0]["formats"][0]["url"], **FFMPEG_OPTS), after=lambda e: looper())

    voiceChannel = None
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if (ctx.author.voice != None):
        if voice == None:
            voiceChannel = ctx.author.voice.channel
            await ctx.message.add_reaction("👍")
            await voiceChannel.connect()
    else:
        await ctx.channel.send("Please join a voice channel before using that command.")
        return
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        video = ydl.extract_info(f"ytsearch:{url}", download=False)
        #ydl.download(video)

    while(len(video['entries']))==0:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(f"ytsearch:{url}", download=False)
    queue[ctx.guild.id].append(video)
    print(len(queue[ctx.guild.id]))
    await ctx.channel.send("**Queued: " + video['entries'][0]['title'] + "**")

    if voice.is_playing() and len(queue[ctx.guild.id])>1:
        return
    '''
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    '''
    embed = discord.Embed(title=f"Now Playing: {queue[ctx.guild.id][0]['entries'][0]['title']}.", url=queue[ctx.guild.id][0]["entries"][0]["webpage_url"], color=discord.Colour.from_rgb(102, 25 ,255))
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    await ctx.channel.send(embed=embed)
    if looping[ctx.guild.id]==False:
        voice.play(discord.FFmpegPCMAudio(queue[ctx.guild.id][0]["entries"][0]["formats"][0]["url"], **FFMPEG_OPTS), after=lambda e: remove_song())
    else:
        voice.play(discord.FFmpegPCMAudio(queue[ctx.guild.id][0]["entries"][0]["formats"][0]["url"], **FFMPEG_OPTS), after=lambda e: looper())

@client.command()
async def pause(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.channel.send("**II Paused**")
    else:
        await ctx.channel.send("No audio is currently playing.")

@client.command()
async def resume(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.channel.send("**I> Resumed**")
    else:
        await ctx.channel.send("The audio isn't paused.")

@client.command(aliases=["clear"])
async def stop(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        queue[ctx.guild.id].clear()
        voice.stop()
        await ctx.channel.send("**Stopped.**")
    else:
        await ctx.channel.send("No audio is currently playing.")

@client.command()
async def delete(ctx, num):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    owner_id = 550093700735172608
    if (not ctx.message.author.guild_permissions.administrator) and ctx.message.author.id != owner_id:
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        await ctx.channel.send("Only admins and " + client.get_user(owner_id).mention + " can use this command.")
        return
    try:
        num = int(num)
    except TypeError:
        await ctx.channel.send("The parameter should be an integer.")
        return

    await ctx.channel.purge(limit=num+1)

@client.command()
async def announce(ctx, *, str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    owner_id = 550093700735172608
    if (not ctx.message.author.guild_permissions.administrator) and ctx.message.author.id != owner_id:
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        await ctx.channel.send("Only admins and " + client.get_user(owner_id).mention + " can use this command.")
        return
    await ctx.message.delete()
    await ctx.channel.send(ctx.guild.default_role)
    embed = discord.Embed(title=(str), url = "https://youtu.be/zqflC-as2Qo", color=discord.Colour.from_rgb(102, 25 ,255))
    await ctx.channel.send(embed=embed)

@client.command()
async def whitelist(ctx):
    owner_id = 550093700735172608
    if (not ctx.message.author.guild_permissions.administrator) and ctx.message.author.id != owner_id:
        await ctx.channel.send("Sorry! You lack the permissions to use this command.")
        await ctx.channel.send("Only admins and " + client.get_user(owner_id).mention + " can use this command.")
        return
    if ctx.channel.id in whitelisted_channels:
        whitelisted_channels.remove(ctx.channel.id)
        await ctx.channel.send("This channel has been un-whitelisted.")
        return
    whitelisted_channels.append(ctx.channel.id)
    await ctx.channel.send("This channel has been whitelisted.")

@client.command(aliases=["repeat"])
async def echo(ctx, *, str):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    await ctx.message.delete()
    await ctx.channel.send(str)

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
async def schoolDay(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    num = time.localtime().tm_wday
    if num == 0:
        await ctx.channel.send("Today is a Brown A day.")
        await ctx.channel.send("Cohort A should be present at school.")
    if num == 1:
        await ctx.channel.send("Today is a Gold A day.")
        await ctx.channel.send("Cohort A should be present at school.")
    if num == 2:
        await ctx.channel.send("Today is a VFlex day.")
        await ctx.channel.send("There are no regular classes, but there is collaboration from 10:30 to 12.")
    if num == 3:
        await ctx.channel.send("Today is a Brown B day.")
        await ctx.channel.send("Cohort B should be present at school.")
    if num == 4:
        await ctx.channel.send("Today is a Gold B day.")
        await ctx.channel.send("Cohort B should be present at school.")
    if num > 4:
        await ctx.channel.send("Today is a weekend. No classes.")
    await ctx.channel.send("Note: This is a hidden command.")

@client.command()
async def guilds(ctx):
    for i in client.guilds:
        await ctx.channel.send(i.name + " - " + i.owner.name)
    await ctx.channel.send()

@client.command(aliases=["images", "img"])
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
async def nba(ctx):
    url = "https://www.basketball-reference.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    req = soup.find_all("tr", {"class": "loser"})
    losers_info = []
    for i in req:
        losers_info.append(list(i))

    req = soup.find_all("tr", {"class": "winner"})
    winners_info = []
    for i in req:
        winners_info.append(list(i))

    losers_scores = []
    for i in losers_info:
        losers_scores.append([i[1].text, i[3].text])

    winners_scores = []
    for i in winners_info:
        winners_scores.append([i[1].text, i[3].text])
    embed = discord.Embed(title="NBA Game Scores", description="Latest game scores.",  url="https://www.basketball-reference.com/", color=discord.Colour.from_rgb(102, 25 ,255))

    for i in range(len(winners_scores)):
        embed.add_field(name=f"Game {i+1}" , value=losers_scores[i][0] + ": " + losers_scores[i][1] + "\n" + winners_scores[i][0] + ": " + winners_scores[i][1])

    embed.set_thumbnail(url="https://1.bp.blogspot.com/-pr9n23TVnfw/XHhYFQOhfsI/AAAAAAAAILQ/iNOGcw8U-1QAGSxHe6G9gWIirQyVrwjZwCK4BGAYYCw/s1600/nba%2Blogo.png")
    await ctx.channel.send(embed=embed)

@client.command(aliases=["queue"])
async def q(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    global queue
    if (not ctx.guild.id in queue) or len(queue[ctx.guild.id])==0:
        await ctx.channel.send("**Queue is empty.**")
        queue[ctx.guild.id] = []
        return
    embed = discord.Embed(title="Current Queue", color=discord.Colour.from_rgb(102, 25 ,255))
    embed.add_field(name="Now Playing:", value=queue[ctx.guild.id][0]['entries'][0]['title'], inline=False)
    phrase = ""
    if len(queue[ctx.guild.id]) > 1:
        for num, i in enumerate(queue[ctx.guild.id][1:]):
            phrase += (str(num+1) + ". " + i['entries'][0]['title'] + "\n")
        embed.add_field(name="Up Next:", value=phrase, inline=False)
        embed.set_footer(text=f"{len(queue[ctx.guild.id][1:])} songs in Queue.")
    await ctx.channel.send(embed=embed)

@client.command()
async def skip(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.channel.send("**Skipped**")
    else:
        await ctx.channel.send("No audio is currently playing.")

@client.command()
async def loop(ctx):
    if ctx.channel.id in whitelisted_channels:
        await ctx.channel.send("Sorry! This channel is whitelisted so I can't respond to commands.")
        await ctx.channel.send("Either use 'zx whitelist' to un-whitlist this channel or use another channel.")
        return
    global looping
    if not ctx.guild.id in looping:
        looping[ctx.guild.id] = False
    if looping[ctx.guild.id]==False:
        looping[ctx.guild.id] = True
        await ctx.channel.send("**Looping enabled.**")
    else:
        looping[ctx.guild.id] = False
        await ctx.channel.send("**Looping disabled.**")

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
