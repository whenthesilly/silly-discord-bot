import discord
import random
import os
import sys
import subprocess
import requests
from PIL import Image, ImageFont, ImageDraw
import textwrap
from decouple import config
from uwuipy import uwuipy
import calendar
import time

ts = calendar.timegm(time.gmtime())


owo = uwuipy(ts, 0.3, 0.3, 0.1, 0.5)


def callJokeApi():
    x = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    data = x.json()
    if data["type"] == "single":
        return str(data["joke"])
    elif data["type"] == "twopart":
        return str(data["setup"] + "\n" + data["delivery"])


def getFact():
    x = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
    data = x.json()
    return data["text"]


bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(description="Basic command that greets you. Used to test uptime.")
async def hello(ctx):
    await ctx.respond(f"Omg haiii, {ctx.author} ^w^!")


@bot.slash_command(description="Random number generator. Defaults to 1-10")
async def pickrandom(ctx, min=1, max=10):
    await ctx.respond("Your number is:" + str(random.randint(int(min), int(max))))


@bot.slash_command(
    guild_ids=["1065613788470071337"],
    description="Applies the latest changes globally.",
)
async def reload(ctx):
    await ctx.respond("Reloading...")
    await subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


@bot.slash_command(description="Says what you said! Says what you said!")
async def echo(ctx, text):
    message = text.replace("@", "@​")
    await ctx.respond(f"You said: {message}")


@bot.slash_command(description="Tells a joke!")
async def joke(ctx):
    await ctx.respond(callJokeApi())


@bot.slash_command(description="Shows current changelogs.")
async def changelogs(ctx):
    with open("/home/pi/discordBot/changelogs.txt", "r") as f:
        data = f.read()
        await ctx.respond(data)


@bot.slash_command(description="Credits people smarter than me for what they did.")
async def credits(ctx):
    with open("/home/pi/discordBot/credits.txt", "r") as f:
        data = f.read()
        await ctx.respond(data)


@bot.slash_command(
    description="Makes the silly garflid image speak (image by @willy on wasteof)"
)
async def garfild(ctx, text: str):
    font = ImageFont.truetype("/home/pi/discordBot/font.ttf", 30)
    # font = ImageFont.load_default()
    img = Image.open("/home/pi/discordBot/pic.jpg")
    cx, cy = (325, 100)
    lines = textwrap.wrap(text, width=17)
    w, h = font.getsize(text)
    y_offset = (len(lines) * h) / 2
    y_text = cy - (h / 2) - y_offset
    for line in lines:
        w2, h2 = font.getsize(line)
        draw = ImageDraw.Draw(img)

        draw.text((cx - (w2 / 2), y_text), line, fill=(0, 0, 0), font=font)
        img.save("/home/pi/discordBot/edit.jpg")
        y_text += h2

    await ctx.respond(file=discord.File("/home/pi/discordBot/edit.jpg"))


@bot.slash_command(description="Links to the github")
async def github(ctx):
    await ctx.respond("https://github.com/reidthepog/Reid-s-discord-bot")


@bot.slash_command(description="Gives you a random useless fact.")
async def uselessfact(ctx):
    await ctx.respond(getFact())


@bot.slash_command(description="uwuifies y-y-youw t-t-t-text.")
async def uwu(ctx, msg):
    await ctx.respond(owo.uwuify(msg))


# @bot.slash_command(description = "meow miaw purr nya ")


token = config("TOKEN")
bot.run(token)
