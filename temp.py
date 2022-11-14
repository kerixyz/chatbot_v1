import os
import discord
from discord.ext import commands

#client is our connection to discord
client = discord.Client(intents=discord.Intents.default())

#on_ready is an event when the bot has logged in and finished set things up
@client.event
async def on_ready():
  print("I'm logged in as", client.user)

#on_message is when the bot received a message
@client.event
async def on_message(message):
  # if message.author != client.user:
  #   await message.channel.send(message.content[::-1])

  if message.content.startswith('hi'):
    await convo_no_1(message)

async def convo_no_1(message):
    # No in first prompt
    message.channel.send("Thank you!")

    return None


#keep_alive()
my_secret = os.environ['DISCORD_BOT_TOKEN']
client.run(my_secret)
