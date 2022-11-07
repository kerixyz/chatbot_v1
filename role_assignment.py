import os, re, discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = 711789671876919408  # insert server id

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


async def dm_about_roles(member):
    print(f"DMing {member.name}...")

    await member.send(f"""Hi {member.name}, welcome to {member.guild.name}! 
        
Which of these languages do you use:
        
* solo (🧍)
* group (🧑‍🤝‍🧑)

Reply to this message with one of the feeds or emojis above so I can assign you the right roles on our server.

Reply with the name or emoji of a language you're currently using and want to stop and I'll remove that role for you.
""")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_member_join(member):
    await dm_about_roles(member)


async def assign_roles(message):
    print("Assigning roles...")

    groups = set(re.findall("solo|group", message.content, re.IGNORECASE))

    groups_emojis = set(re.findall("\U0001F9CD|\U0001F9D1", message.content))
    # https://unicode.org/emoji/charts/full-emoji-list.html

    # Convert emojis to names
    for emoji in groups_emojis:
        {
            "\U0001F9CD": lambda: groups.add("solo"),
            "\U0001F9D1": lambda: groups.add("group")
        }[emoji]()

    if groups:
        server = bot.get_guild(SERVER_ID)

        # <-- RENAMED VARIABLE + LIST CHANGED TO SET
        new_roles = set(
            [discord.utils.get(server.roles, name=groups) for group in groups])

        member = await server.fetch_member(message.author.id)

        # NEW CODE BELOW
        current_roles = set(member.roles)

        roles_to_add = new_roles.difference(current_roles)
        roles_to_remove = new_roles.intersection(current_roles)

        try:
            await member.add_roles(*roles_to_add,
                                   reason="Roles assigned by KehreeBot.")
            await member.remove_roles(*roles_to_remove,
                                      reason="Roles revoked by KehreeBot.")
        except Exception as e:
            print(e)
            await message.channel.send("Error assigning/removing roles.")
        else:
            if roles_to_add:
                await message.channel.send(
                    f"You've been assigned the following role{'s' if len(roles_to_add) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_add]) }"
                )

            if roles_to_remove:
                await message.channel.send(
                    f"You've lost the following role{'s' if len(roles_to_remove) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_remove]) }"
                )

    else:
        await message.channel.send("sorry im confused")


@bot.event
async def on_message(message):
    print("Saw a message...")

    if message.author == bot.user:
        return  # prevent responding to self

    # NEW CODE BELOW
    # Assign roles from DM
    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return
    # NEW CODE ABOVE

    # Respond to commands
    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)

    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)


print(bot.get_guild(SERVER_ID))
print(bot.get_channel(1036700090993213481))
bot.run(DISCORD_TOKEN)
 