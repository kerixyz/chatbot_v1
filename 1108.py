import discord
import random
import asyncio
import os
from discord.ext import commands



## Discord Section ##
os.environ['DISCORD_BOT_TOKEN'] = ''
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

#on_ready is an event when the bot has logged in and finished set things up
@bot.event
async def on_ready():
  print("I'm logged in as", bot.user)


@bot.command()
async def feedback(ctx):
    await ctx.send('What worked well or not well in my recent stream?')

@bot.command()
async def DM(ctx, user:discord.User, *, message=None):
  message = message or "This Message is sent via DM"
  await user.send(message)


@bot.event
async def on_message(ctx):
  if ctx.content == 'help me':
    
    #user id of the streamer only
    user = await bot.fetch_user(207331288519147522)

    if user is not None:
        if user.dm_channel is None:
          await user.create_dm()

        await user.dm_channel.send("someone needs help")



my_secret = os.environ['DISCORD_BOT_TOKEN']
bot.run(my_secret)
