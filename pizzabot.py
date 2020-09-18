# invite link:
# https://discord.com/api/oauth2/authorize?client_id=754851728981229649&permissions=67648&scope=bot

import discord
import random
import re

token = open("token.txt", "r").read() # concealing token

client = discord.Client()

male = 'first_name_male.txt' # male name file
female = 'first_name_female.txt' # female name file
last = 'last_name.txt' # last name name file
pizzatoppings = 'pizzatoppings.txt' # pizza toppings file

def random_name(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def random_topping(fname, ingredients):
    toppings = open(fname).read().splitlines()
    return random.sample(toppings, ingredients)

@client.event # event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}") # chat log for testing

    if re.findall(r"(?i)\bpizza\b", message.content.lower()):  # adds reaction whenever "pizza" is mentioned
        await message.add_reaction("\U0001F355")

    elif "!firstmale" in message.content.lower():
        await message.channel.send(f"```{random_name(male)}```")

    elif "!firstfemale" in message.content.lower():
        await message.channel.send(f"```{random_name(female)}```")

    elif "!fullmale" in message.content.lower():
        await message.channel.send(f"```{random_name(male)} {random_name(last)}```")

    elif "!fullfemale" in message.content.lower():
        await message.channel.send(f"```{random_name(female)} {random_name(last)}```")

    elif "!football" in message.content.lower(): # returns link for scores (web scrape eventually)
        await message.channel.send("https://sportsdata.usatoday.com/football/nfl/scores")
    
    elif re.match(r"(?i)^[!]?toppings\s?[1-7]?$", message.content.lower()):

        if re.fullmatch(r"(?i)^[!]?toppings$", message.content.lower()):
            ingredients = random.randint(1, 3) # if no modifier is given, a random number between 1 and 3 is chosen for ingredients

        else:
            ingredients = int(re.findall(r"\b[1-7]\b", message.content.lower())[0]) # converting !toppings # into just a #
    
        topping_list = random_topping(pizzatoppings, ingredients) # creating list for toppings

        your_pizza = "" # creating string for output
        your_pizza = ", ".join(topping_list[0:-1:]) # forming a string with everything but last ingredient because grammar
        
        if ingredients == 1: # 1 ingredient
            await message.channel.send(f"You should order a pizza with {topping_list[0]}.")

        elif ingredients == 2: # 2 ingredients
            your_pizza = your_pizza + " and " + topping_list[-1] # adding back last ingredient
            await message.channel.send(f"You should order a pizza with {your_pizza}.")

        else:  # for ingredients between 3 and 7
            your_pizza = your_pizza + ", and " + topping_list[-1] # adding back last ingredient
            await message.channel.send(f"You should order a pizza with {your_pizza}.")

    elif "!toppings" in message.content.lower(): # catches all user user input for !toppings
        await message.channel.send("You need to only use a single number between 1 and 7.")

client.run(token)