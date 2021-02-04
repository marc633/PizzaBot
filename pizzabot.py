import random
import re
import asyncio
import discord
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix = '!')
token = open("token.txt", "r").read() # concealing token

male = 'first_name_male.txt' # male name file
female = 'first_name_female.txt' # female name file
last = 'last_name.txt' # last name name file
bslist = 'bs.txt' # bullshit list
gamelist = 'games.txt' # game list

#VARIABLES
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#CLASSES
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.33):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url):
        data = ytdl.extract_info(url, download=False)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] 
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#FUNCTIONS
def make_pizza(ingredients):
    pizzatoppings = 'pizzatoppings.txt' # pizza toppings file

    topping_list = random_topping(pizzatoppings, ingredients) # creating list for toppings

    your_pizza = "" # creating string for output
    your_pizza = ", ".join(topping_list[0:-1:]) # forming a string with everything but last ingredient because grammar
        
    if ingredients == 1: # 1 ingredient
        return f"You should order a pizza with {topping_list[0]}."

    elif ingredients == 2: # 2 ingredients
        your_pizza = your_pizza + " and " + topping_list[-1] # adding back last ingredient
        return f"You should order a pizza with {your_pizza}."

    else:  # for ingredients between 3 and 7
        your_pizza = your_pizza + ", and " + topping_list[-1] # adding back last ingredient
        return f"You should order a pizza with {your_pizza}."

def random_name(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def random_topping(fname, ingredients):
    toppings = open(fname).read().splitlines()
    return random.sample(toppings, ingredients)

#BOT CONNECTING
@client.event # event decorator/wrapper
async def on_ready():
    activity = discord.Activity(name="Pizza Cook", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"DING! {client.user} has emerged from the oven.")

#EVENTS
@client.event
async def on_message(message):
    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}") # chat log for testing

    if re.findall(r"(?i)\bpizzas?\b", message.content.lower()):  # adds reaction whenever "pizza" is mentioned
        await message.add_reaction("\U0001F355")
    await client.process_commands(message)

#COMMANDS
@client.command()
async def game(ctx, action, *args):
    gamename = " ".join(args)
    if action == "add":
        with open(gamelist, 'a') as file:
            file.writelines(f'{gamename}\n')
        await ctx.send(f"```Added {gamename} to your list of Happy Hour games```")
    elif action == "remove":
        with open(gamelist, 'r') as ofile:
            lines = ofile.readlines()
        with open(gamelist, 'w') as nfile:
            for line in lines:
                if line.strip("\n") != gamename:
                    nfile.write(line)
        await ctx.send(f"```Removed {gamename} from your list of Happy Hour games```")
    elif action == "random":
        result = open(gamelist).read().splitlines()
        await ctx.send(f'I choose...\n```{random.choice(result)}```')
    elif action == "list":
        # await ctx.send(gamelist.read().strip())
        games = open(gamelist).read()
        await ctx.send(f"```{games}```")
    else:
        await ctx.send("Please use a valid action:\n```!game add gamename\n!game remove gamename\n!game random\n!game list```")

@client.command()
async def firstmale(ctx):
    await ctx.send(f"```{random_name(male)}```")

@client.command()
async def firstfemale(ctx):
    await ctx.send(f"```{random_name(female)}```")

@client.command()
async def fullmale(ctx):
    await ctx.send(f"```{random_name(male)} {random_name(last)}```")

@client.command()
async def fullfemale(ctx):
    await ctx.send(f"```{random_name(female)} {random_name(last)}```")

@client.command()
async def football(ctx):
    await ctx.send("https://sportsdata.usatoday.com/football/nfl/scores")

@client.command()
async def toppings(ctx, ingredients=""):    
    try:
        if ingredients == "": ingredients = random.randint(1,3)
        ingredients = int(ingredients)

        if ingredients > 7 or ingredients < 1:
            raise Exception
        await ctx.send(make_pizza(ingredients))

    except ValueError:
        await ctx.send("You must use only numbers.")

    except Exception:
        await ctx.send("You must only use a single number between 1 and 7.")

@client.command()
async def prand(ctx, *args):
    argstring = " ".join(args)
    option_regex = re.compile(r'^(?P<count>[1-9]?[0-9]*)?\s?(?P<choices>[a-zA-Z0-9?!, ]*)$')
    options = option_regex.search(argstring)

    count = options.group('count')
    count = 1 if count == '' else int(count)
    
    choices = options.group('choices').split(',')
    results = ', '.join(random.sample(choices, count))
    await ctx.send(f'I choose pizz... I mean:\n```{results}```')
    
    with open(bslist, 'a') as file:
        file.writelines("%s\n" % c for c in choices)

@client.command()
async def srand(ctx, *args):
    result = open(bslist).read().splitlines()
    await ctx.send(f'I choose pizz... I mean:\n```{random.choice(result)}```')

# PLAYBACK COMMANDS
@client.command()
async def play(ctx, url):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()

        player = await YTDLSource.from_url(url)
        ctx.voice_client.play(player)
        await ctx.send(f'Now playing on PizzaBot Radio: {player.title}\n```Playback Commands:\n!volume [1-100]\n!stop```')
    except AttributeError:
        await ctx.send("You must join a channel before using the !play command.")        

@client.command()
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        await ctx.send("Not connected to a voice channel.")
    
    if volume > 100: volume = 100
    if volume < 1: volume = 1

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

@client.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

client.run(token)