import os
import random
import re
import asyncio
import discord
import requests
import pytz
from hockey import game_search, scores
from datetime import datetime, timedelta
from discord.ext import commands
# import youtube_dl

owners = [193721090755788801]
client = commands.Bot(command_prefix = '!', case_insensitive=True, owner_ids = set(owners))
# token = open("token.txt", "r").read() # concealing token # NOT NEEDED FOR HEROKU

male = 'first_name_male.txt' # male name file
female = 'first_name_female.txt' # female name file
last = 'last_name.txt' # last name name file
bslist = 'bs.txt' # bullshit list
gamelist = 'games.txt' # game list

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
    if re.findall(r"(?i)\bpizzas?\b", message.content.lower()):  # adds reaction whenever "pizza" is mentioned
        await message.add_reaction("\U0001F355")
    await client.process_commands(message)

#COMMANDS
@client.command(brief='This will display and add to happy hour games.')
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
        games = open(gamelist).read()
        await ctx.send(f"```{games}```")
    else:
        await ctx.send("Please use a valid action:\n```!game add gamename\n!game remove gamename\n!game random\n!game list```")

@client.command(brief="Random first or full name for males or females.")
async def name(ctx, style="rand", gender="rand"):
    style_opt = ('first', 'full')
    gender_opt = ('male', 'female')
    if style == "rand": style = random.choice(style_opt)
    if gender == "rand": gender = random.choice(gender_opt)
    style, gender = style.lower(), gender.lower()

    if style not in style_opt or gender not in gender_opt:
        await ctx.send("```Must be in this format:\n!name [first|full|rand] [male|female|rand]\nYou may also just use !name for all random.```")

    elif style == 'first':
        if gender == 'male':
            await ctx.send(f"```{random_name(male)}```")
        else:
            await ctx.send(f"```{random_name(female)}```")

    else:
        if gender == 'male':
            await ctx.send(f"```{random_name(male)} {random_name(last)}```")
        else:
            await ctx.send(f"```{random_name(female)} {random_name(last)}```")

@client.command()
async def football(ctx):
    await ctx.send("https://sportsdata.usatoday.com/football/nfl/scores")

@client.command(brief='Gives a pizza with random toppings.')
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

@client.command(brief='Selects a random choice from those supplied.')
async def rand(ctx, *args):
    if 'forza' == args[0].lower():
        forza_class = ('D', 'C', 'B', 'A', 'S1', 'S2', 'X')
        forza_race = ('Road', 'Dirt', 'Cross Country', 'Street', 'Drag')
        forza_class_choice = random.choices(forza_class, weights=[55, 160, 210, 210, 160, 125, 75], k=1)[0]
        forza_race_choice = random.choices(forza_race, weights=[2475, 2475, 2475, 2475, 100], k=1)[0]
 
        if len(args) == 2 and args[1].upper() in forza_class:
            forza_class_choice = args[1].upper()
        
        await ctx.send(f'I choose...\n```{forza_race_choice} Racing with \'{forza_class_choice}\' ranked vehicles.```')

    else:
        choices = " ".join(args)
        choices = choices.split(',')
        choices = [i for i in choices if i != '']

        try:
            if len(choices) < 2:
                await ctx.send('You must give me at least 2 choices.')
            else:
                result = random.choice(choices).strip()
                await ctx.send(f'I choose...\n```{result}```')
        except IndexError:
            await ctx.send('You didn\'t provide any choices.')

@client.command(brief='Multiple random choices from those supplied.')
async def mrand(ctx, count=None, *args):
    try:
        count = int(count)
    except ValueError:
        await ctx.send("You must only use numbers for your choices, for example:\n```!mrand 2 first, second, third```")
        return
    except TypeError:
        await ctx.send("You must provide a count and choices, for example:\n```!mrand 2 first, second, third```")
        return

    choices = "".join(args)
    choices = choices.replace(', ', ',')
    choices = choices.split(',')
    choices = [i for i in choices if i != '']
    
    try:
        if len(choices) <= count:
            await ctx.send(f'You must provide more choices ({len(choices)} given) than your desired results ({count} given).')
        else:
            result_list = random.sample(choices, count)
            result = '\n'
            for i in result_list:
                result += i + '\n'
            await ctx.send(f'I choose...\n```{result}```')
    except IndexError:
        await ctx.send('You didn\'t provide any choices.')
    except ValueError:
        await ctx.send('You didn\'t provide enough choices.')

@client.command(brief='Really bad random, who knows what it\'s doing?')
async def srand(ctx, *args):
    result = open(bslist).read().splitlines()
    await ctx.send(f'I choose pizz... I mean:\n```{random.choice(result)}```')

@client.command(brief='Gives hockey scores for yesterday/today/tomorrow')
async def hockey(ctx, *, args=None):
    argtuple = None
    if args: argtuple = tuple(args.split(' '))

    pst = pytz.timezone('America/Los_Angeles')
    
    modopt = ["0", "+1", "-1", "today", "tomorrow", "yesterday"]
    if argtuple == None:
        mod = "0"
        teams_req = None
    elif argtuple[0].lower() in modopt:
        mod = argtuple[0]
        teams_req = argtuple[1:]
    else:
        mod = "0"
        teams_req = argtuple

    if mod == "-1" or mod.lower() == "yesterday": mod = -1
    elif mod == "+1" or mod.lower() == "tomorrow": mod = 1
    else: mod = 0

    date = datetime.date(datetime.now(pst) + timedelta(days=mod)).strftime("%Y-%m-%d")
    url = f"https://statsapi.web.nhl.com/api/v1/schedule?startDate={date}&endDate={date}&expand=schedule.linescore"

    response = requests.get(url, headers={"Accept": "application/json"})

    data = response.json()
    game_count = data['totalGames']

    if game_count == 0:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%-m/%-d")
        await ctx.send(f'There are no games scheduled on {date}!')

    elif teams_req:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%-m/%-d")
        games = data['dates'][0]['games']
        games_req = game_search(games, game_count, teams_req)
        msg = scores(games, game_count, games_req)
        if msg == "":
            teamsout = "\n"
            for i in teams_req: teamsout += i + '\n'
            msg = f"There were no games matching your search criteria on {date}:\n```{teamsout}```"
        await ctx.send(msg)
    
    else:
        games_req = [i for i in range(game_count)]
        games = data['dates'][0]['games']
        await ctx.send(scores(games, game_count, games_req))

@client.command(brief='DnD style dice roller.')
async def roll(ctx, *args):
    dice_input = " ".join(args)
    valid_input = re.search(
                r"^[1-9][0-9]{0,2}[dD][1-9][0-9]{0,2}( ?[\+\-][0-9]+)?( [dD][lL])?( [dD][hH])?$|^(dndstats)$", dice_input)

    if valid_input != None:
        options = re.split(r'[dD\+\-]', dice_input)
        dice_mod = re.findall(r'[\+\-]', dice_input)

        if 'stats' in options:
            stats = []
            def dndstats():
                rollcount = 0
                roll_out = ""
                while rollcount < 6:
                    roll_total = 0
                    badrolls = []
                    while roll_total < 8:
                        roll = [random.randint(1, 6) for val in range(4)]
                        lowroll = min(roll)
                        roll.remove(lowroll)
                        roll_total = sum(roll)
                        if roll_total < 8:
                            badrolls.append(roll_total)
                    stats.append(roll_total)
                    roll_full = f"[{roll[0]}, {roll[1]}, {roll[2]}, ~~{lowroll}~~]"
                    if badrolls:
                        roll_out += f'{roll_full} -- TOTAL: {roll_total} -- BADROLLS: {badrolls}\n'
                    else:    
                        roll_out += f'{roll_full} -- TOTAL: {roll_total}\n'
                    rollcount += 1
                roll_out += f'\nStats: {stats}'
                return roll_out

            await ctx.send(f'{dndstats()}')

        else:
            roll = [random.randint(1, int(options[1])) for val in range(int(options[0]))]

            matches = ['l','h']
            if all(any(i in j for j in options) for i in matches):
                roll.remove(min(roll))
                roll.remove(max(roll))

            elif 'l' in options: 
                roll.remove(min(roll))

            elif 'h' in options: 
                roll.remove(max(roll))

            
            if "+" in dice_mod:
                roll_total = sum(roll) + int(options[2])

            elif "-" in dice_mod:
                roll_total = sum(roll) - int(options[2])

            else:
                roll_total = sum(roll)
                options.insert(2, 0)  # for printing purposes
                dice_mod.append("+")  # for printing purposes
            
            await ctx.send(f"{roll} {dice_mod[0]}{options[2]} -- TOTAL: {roll_total}")

@client.command(brief='Reminds in minutes or \'tomorrow\' with message')
async def remindme(ctx, rtime=None, *, args='You requested a reminder.'):
    try:
        if rtime.lower() == 'tomorrow':
            await asyncio.sleep(86400)
        elif int(rtime) <= 1440 and int(rtime) > 0:
            rtime = int(rtime) * 60
            await asyncio.sleep(rtime)
        else:
            await ctx.send('Reminders must be between 1 minute and a full day.')
            return
        await ctx.send(f'{ctx.author.mention}:\n{args}')
    except ValueError:
        await ctx.send('You must use any of these formats:\n```!remindme [minutes] [message]\n!remindme tomorrow [message]```')
    except AttributeError:
        await ctx.send('You must enter a valid remind time.')

#HIDDEN OWNER COMMANDS
# @client.command(hidden=True)
# @commands.is_owner()
# async def say(ctx, *, args):
#     await ctx.send(args)

@client.command(hidden=True)
@commands.is_owner()
async def say(ctx, channel, *, args):
    try:
        channel = await commands.TextChannelConverter().convert(ctx, channel)
        message = args
        await channel.send(message)
    except commands.errors.ChannelNotFound:
        await ctx.send('You must send to an active chat channel. EX:\n!say general hi')
    except Exception as e:
        await ctx.send(f'Something went wrong: {e}')

# client.run(token) # NOT NEEDED FOR HEROKU
client.run(os.environ['BOT_TOKEN'])