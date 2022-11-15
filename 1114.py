#import stuff
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

import discord
import random
import asyncio
import os
from discord.ext import commands


# initialize a bunch of stuff
os.environ['DISCORD_BOT_TOKEN'] = ''
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

analyzer = SentimentIntensityAnalyzer()

## sentiment analyzer code
def sentiment_analyzer_scores(text):
    score = analyzer.polarity_scores(text)

    lb = score['compound']

    if lb >= 0.05: 
        return 'postiive'

    elif (lb > - 0.05) and (lb < 0.05):
        return 'neutral'

    else:
        return 'negative'

## constructive model analyzer code

## discord code

#on_ready is an event wshen the bot has logged in and finished set things up
@bot.event
async def on_ready():
  print("I'm logged in as", bot.user)


## initial line of questioning

## strengths: what are you enjoying in this stream? please explain or give examples

## suggestions: what changes could be made that would assist your enjoyment?

### constructive / non-constructive

# my_secret = os.environ['DISCORD_BOT_TOKEN']
# bot.run(my_secret)

print(sentiment_analyzer_scores('ur mom'))
