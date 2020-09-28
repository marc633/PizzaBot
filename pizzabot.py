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

@client.event # event decorator/wrapper
async def on_ready():
    activity = discord.Game(name="P-P-P-PIZZA!", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"DING! Your fresh {client.user} is ready.")

@client.event
async def on_message(message):
    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}") # chat log for testing

    if re.findall(r"(?i)\bpizza\b", message.content.lower()):  # adds reaction whenever "pizza" is mentioned
        await message.add_reaction("\U0001F355")
    await client.process_commands(message)

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

client.run(token)