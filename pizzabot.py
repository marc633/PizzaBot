# invite link:
# https://discord.com/api/oauth2/authorize?client_id=754851728981229649&permissions=67648&scope=bot

import discord
import random

token = open("token.txt", "r").read() # concealing token

client = discord.Client()

male = 'male.txt'
female = 'female.txt'
last = 'last.txt'

def random_name(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

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
    

client.run(token)