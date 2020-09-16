# invite link:
# https://discord.com/api/oauth2/authorize?client_id=754851728981229649&permissions=67648&scope=bot

import discord
import random

token = open("token.txt", "r").read() # concealing token

client = discord.Client()

male = 'male.txt' # male name file
female = 'female.txt' # female name file
last = 'last.txt' # last name name file
pizzatoppings = 'pizzatoppings.txt' # pizza toppings file

def random_name(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

def random_topping(fname):
        toppings = open(fname).read().splitlines()
        return random.choice(toppings)

@client.event # event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    # if "!pizza" in message.content.lower() and message.author.name != "PizzaBot":
    #     await message.channel.send("PIZZA! P-P-P-Pizza")

    if "pizza" in message.content.lower(): # adds reaction whenever "pizza" is mentioned
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
    
    elif "!toppings" in message.content.lower():

        if len(message.content.lower()) > 9: # check for modifier
            command = message.content.lower().split()
            ingredients = int(command[1])

        else:
            ingredients = 1

        topping_list = [random_topping(pizzatoppings) for i in range(ingredients)] # list for random ingredients

        your_pizza = "" # string to populate for output
        your_pizza = ", ".join(topping_list[0:-1:]) # add all but last item to string

        if ingredients > 7:
            await message.channel.send("Never thought I'd say this... go eat a salad.")

        elif ingredients < 0:
            await message.channel.send("You should order a basket of breadsticks... with marinara dipping sauce, of course.")
        
        elif ingredients == 1:
            await message.channel.send(f"You should order a pizza with {topping_list[0]}.")

        elif ingredients == 2:
            your_pizza = your_pizza + " and " + topping_list[-1] # grammarbot
            await message.channel.send(f"You should order a pizza with {your_pizza}.")

        else:  # 3-7 results
            your_pizza = your_pizza + ", and " + topping_list[-1] # grammarbot
            await message.channel.send(f"You should order a pizza with {your_pizza}.")

client.run(token)