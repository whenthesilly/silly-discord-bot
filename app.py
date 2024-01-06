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
import pytz
from suncalc import get_position
from datetime import datetime as dt
import datetime
import wasteof

ts = calendar.timegm(time.gmtime())


owo = uwuipy(ts, 0.3, 0.3, 0.1, 0.5)


def callJokeApi():
    x = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")

    if x.status_code != 200:
        return "Sowwy, I can't tell you a joke right now. Try again later."

    data = x.json()
    if data["type"] == "single":
        return str(data["joke"])
    elif data["type"] == "twopart":
        return str(data["setup"] + "\n" + data["delivery"])


def getFact():
    x = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")

    if x.status_code != 200:
        return "Sowwy, I can't tell you a fact right now. Try again later."

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
async def pickrandom(ctx, min: int = 1, max: int = 10):
    await ctx.respond("Your number is:" + str(random.randint(int(min), int(max))))


@bot.slash_command(
    guild_ids=["1065613788470071337"],
    description="Applies the latest changes globally.",
)
async def reload(ctx):
    await ctx.respond("Reloading...")
    await subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


@bot.slash_command(description="Says what you said! Says what you said!")
async def echo(ctx, text: str):
    message = text.replace("@", "@​")
    await ctx.respond(f"You said: {message}")


@bot.slash_command(description="Tells a joke!")
async def joke(ctx):
    await ctx.respond(callJokeApi())


@bot.slash_command(description="Shows current changelogs.")
async def changelogs(ctx):
    with open("./changelogs.txt", "r") as f:
        data = f.read()
        await ctx.respond(data)


@bot.slash_command(description="Credits people smarter than me for what they did.")
async def credits(ctx):
    with open("./credits.txt", "r") as f:
        data = f.read()
        await ctx.respond(data)


@bot.slash_command(
    description="Makes the silly garflid image speak (image by @willy on wasteof)"
)
async def garfild(ctx, text: str):
    font = ImageFont.truetype("./font.ttf", 30)
    # font = ImageFont.load_default()
    img = Image.open("./pic.jpg")
    cx, cy = (325, 100)
    lines = textwrap.wrap(text, width=17)
    w, h = font.getsize(text)
    y_offset = (len(lines) * h) / 2
    y_text = cy - (h / 2) - y_offset
    for line in lines:
        w2, h2 = font.getsize(line)
        draw = ImageDraw.Draw(img)

        draw.text((cx - (w2 / 2), y_text), line, fill=(0, 0, 0), font=font)
        img.save("./edit.jpg")
        y_text += h2

    await ctx.respond(file=discord.File("./edit.jpg"))


@bot.slash_command(description="Links to the github")
async def github(ctx):
    await ctx.respond("https://github.com/whenthesilly/silly-discord-bot")


@bot.slash_command(description="Gives you a random useless fact.")
async def uselessfact(ctx):
    await ctx.respond(getFact())


@bot.slash_command(description="uwuifies y-y-youw t-t-t-text.")
async def uwu(ctx, msg):
    await ctx.respond(owo.uwuify(msg))


@bot.slash_command(description="meow miaw purr nya~")
async def cat(ctx):
    r = requests.get("https://cataas.com/cat")
    open("./cat.jpg", "wb").write(r.content)
    await ctx.respond(file=discord.File("./cat.jpg"))


@bot.slash_command(
    description="get the azimuth angle (https://en.wikipedia.org/wiki/Azimuth) of the sun in any place on earth"
)
async def azimuth(ctx, latitude: float, longitude: float, timezone: str):
    utcNow = datetime.datetime.utcnow()
    try:
        tz = pytz.timezone(timezone)
        now = utcNow.astimezone(tz)
        sunPos = get_position(now, latitude, longitude)
        await ctx.respond(f"Sun azimuth angle: {sunPos['azimuth']}")
    except Exception as e:
        await ctx.respond(
            f"An error occured. Try different coordinates or timezone. \n ```{e}```"
        )


@bot.slash_command(description="displays wasteof user info")
async def womuser(ctx, user: str):
    if not wasteof.users.isUserAvailable(username=user):
        info = wasteof.users.get(username=user)
        name = info["name"]

        if info["verified"]:
            name = name + " <:Verified:1115381015943319612>"
        if info["permissions"]["admin"]:
            name = name + " <:Admin:1115380983395532860>"
        if info["beta"]:
            name = name + " <:Beta:1117853412994846730>"
        if info["online"]:
            name = name + "  🟢"

        match info["color"]:
            case "red":
                colour = 0xF87171
            case "orange":
                colour = 0xFB923C
            case "yellow":
                colour = 0xFACC15
            case "green":
                colour = 0x4ADE80
            case "teal":
                colour = 0x2DD4BF
            case "blue":
                colour = 0x60A5FA
            case "indigo":
                colour = 0x818CF8
            case "fuchsia":
                colour = 0xE879F9
            case "gray":
                colour = 0x9CA3AF
            case "pink":
                colour = 0xEC4899
            case _:
                colour = 0x818CF8
                colerror = info["color"]
                print(
                    f"{user}'s colour {colerror} not recognized. defaulting to indigo."
                )

        embed = discord.Embed(
            title=name,
            description=info["bio"],
            color=colour,
        )
        if "history" in info:
            timestamp = info["history"]["joined"] // 1000
            embed.add_field(
                name="Join date",
                value=f"<t:{timestamp}> (<t:{timestamp}:R>)",
                inline=True,
            )
        embed.add_field(name="Followers", value=info["stats"]["followers"], inline=True)
        embed.add_field(name="Following", value=info["stats"]["following"], inline=True)
        embed.add_field(name="Posts", value=info["stats"]["posts"], inline=True)
        embed.set_thumbnail(url=f"https://api.wasteof.money/users/{user}/picture")
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("User not found!", ephemeral=True)


token = config("TOKEN")
bot.run(token)
