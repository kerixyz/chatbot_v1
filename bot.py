# bot.py
import os
import json

import random
import discord

from convo_flow import *

from discord.ext import commands

import asyncio # To get the exception

with open('env.json', 'r') as fp:
    env = json.load(fp)
    TOKEN = env['DISCORD_TOKEN']

bot = commands.Bot(command_prefix = '$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test', help='Test connection function.')
async def roll(ctx):
    await ctx.send("Surprise mothafucka")

@bot.command(name='questions', help='Get example questions')
async def ask_qs(ctx):
    themes = find_questions()
    await ctx.send(themes)


@bot.command(name='feedback', help='Get feedback')
async def _command(ctx):
    # How many to poll
    await ctx.send(f"Time to get some feedback! How many viewers do you want to poll?")
    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        poll_count = await bot.wait_for("message", check=check, timeout=10) # 30 seconds to reply
        poll_count = int(poll_count.content)
    except asyncio.TimeoutError:
        await ctx.send("Are you there?")

    await ctx.send(f"What question do ou want to ask?")
    try:
        question = await bot.wait_for("message", check=check, timeout=10) # 30 seconds to reply
        question = question.content
    except asyncio.TimeoutError:
        await ctx.send("Are you there?")

    await ctx.send(f"Polling {poll_count:,} viewers to ask: \n```{question}```")

bot.run(TOKEN)