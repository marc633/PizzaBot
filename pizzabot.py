import discord
import config

client = discord.Client()

@client.event # event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if "pizza" in message.content.lower() and message.author.name != "PizzaBot":
        await message.channel.send("PIZZA! P-P-P-Pizza")

    if "!football" in message.content.lower():
        await message.channel.send("https://www.nfl.com/schedules/")
    

client.run(config.token())