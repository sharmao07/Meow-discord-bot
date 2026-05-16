import discord
from discord.ext import commands # Import the commands extension
import requests
import os
from dotenv import load_dotenv
import certifi
import random
import json
import asyncio
import time
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True          # This stays ON now
intents.message_content = True 

bot = commands.Bot(command_prefix='?', intents=intents)

# SSL issue
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
LOG_CHANNEL_ID = 1501630207075811418

def load_vault():
    
    if not os.path.exists("vault.json"):
        with open("vault.json", "w") as f:
            json.dump({}, f)
        return {}
        
    try:
        with open("vault.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading vault: {e}")
        return {}

def save_vault(data):
  
    with open("vault.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    
@bot.event
async def on_message(message):
    if message.author == bot.user and not message.content.startswith('?'):
        return

    
    if message.guild is None:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            try:
                log_channel = await bot.fetch_channel(LOG_CHANNEL_ID)
            except:
                pass
            
        if log_channel:
            
            is_reply = message.author == bot.user
            title = "📤 Bot Reply Sent" if is_reply else "📩 New DM Received"
            color = discord.Color.green() if is_reply else discord.Color.blue()
            author_info = f"To: {message.channel}" if is_reply else f"{message.author} ({message.author.id})"

            
            embed = discord.Embed(
                title=title, 
                description = str(message.content) if message.content else "(No text content)", 
                color=color
            )
            embed.set_author(name=author_info)

            if not message.content and not message.attachments and not message.stickers:
                embed.description = "✨ (Contains a custom emoji or system component)"

            
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
                
                if len(message.attachments) > 1:
                    extra_links = "\n".join([a.url for a in message.attachments[1:]])
                    embed.add_field(name="📎 Extra Attachments", value=extra_links)

            if message.stickers:
                sticker_url = message.stickers[0].url
                # If no image attachment exists, show the sticker as the main image
                if not message.attachments:
                    embed.set_image(url=sticker_url)
                else:
                    embed.add_field(name="🎨 Sticker", value=f"[View Sticker]({sticker_url})")

            await log_channel.send(embed=embed)
        
        if message.author == bot.user:
            return

    await bot.process_commands(message)


@bot.command(name="send")
async def send_to_channel(ctx, channel_id: int, *, content: str):
    if ctx.author.id != 778891631591686164: 
        await ctx.send("🚫 Only the bot owner can use this command.")
        return

    try:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(content)
            await ctx.send(f"✅ Message sent to **#{channel.name}**!")
        else:
            await ctx.send("❌ Channel not found. Ensure I am in that server.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")    


def check_permissions(ctx):
    # Get a list of all role names the user has
    user_roles = [role.name.lower() for role in ctx.author.roles]
    
    staff_keywords = [
        "owner", 
        "moderator",
        "friends",
        "event manager", 
        "ticket staff",
        "regular cat person lol"
    ]
    
    is_staff = any(any(key in role for key in staff_keywords) for role in user_roles)
    
    is_bot_channel = "🤖﹒bot-commands" in ctx.channel.name.lower()

    # Logic: Staff can use it everywhere. Non-staff can only use it in bot-commands.
    if is_staff or is_bot_channel:
        return True
    return False


@bot.command(name="reply")
async def reply(ctx, user_id: int, *, content: str):
    # Only you should be able to use this
    if ctx.author.id != 778891631591686164: 
        return

    try:
        user = await bot.fetch_user(user_id)
        await user.send(content)
        await ctx.send(f"✅ Message sent to **{user.name}**!")
    except Exception as e:
        await ctx.send(f"❌ Failed to send message: {e}")


# --- DELTARUNE  ---

@bot.command(name="deltarune")
async def deltarune(ctx):
    if check_permissions(ctx):
        # Using "deltarune pixel" often gets the best game-accurate results
        await send_gif(ctx, "deltarune")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)


@bot.command(name="kris")
async def kris(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "kris deltarune")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

@bot.command(name="susie")
async def susie(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "susie deltarune")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

@bot.command(name="ralsei")
async def ralsei(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "ralsei deltarune")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)        


# --- CHIIKAWA   ---

@bot.command(name="chii")
async def chii(ctx):
    if check_permissions(ctx):
        await send_gif(ctx,  "chiikawa") 
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)
        
@bot.command(name="usagi")
async def chii(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "usagi chiikawa") 
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

@bot.command(name="hachi")
async def hachi(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "hachiware chiikawa")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

@bot.command(name="momo")
async def momo(ctx):
    if check_permissions(ctx):
        momo_gifs = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpmNDlxZWEzNmQ3d2RhNXZscmQxcmpqbmFxaGsxbmZ0aWlscW5ubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tKjowwH3any3aJ4Z79/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpmNDlxZWEzNmQ3d2RhNXZscmQxcmpqbmFxaGsxbmZ0aWlscW5ubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/SH2GeSdLkdyxix7B7S/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpmNDlxZWEzNmQ3d2RhNXZscmQxcmpqbmFxaGsxbmZ0aWlscW5ubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/um5h9GDAoXw2I84h8p/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpmNDlxZWEzNmQ3d2RhNXZscmQxcmpqbmFxaGsxbmZ0aWlscW5ubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TfyTBB8BR9G9hg5uJz/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3oyN3BzNXlrMHlvZGZuaDZ6anFkZjE1dXRvbXJzYnluNmduaWw0YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/OqKrj1ARvDxne2oqFT/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3oyN3BzNXlrMHlvZGZuaDZ6anFkZjE1dXRvbXJzYnluNmduaWw0YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/7gIF4M5CVEhcumZKmH/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3oyN3BzNXlrMHlvZGZuaDZ6anFkZjE1dXRvbXJzYnluNmduaWw0YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/rZmWH1k7ESg3ccoUeP/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NHh1dng2ejVkYWlhazV5Y251empqbjdkdTIyd3p2bzNtZndrbG41OCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/izIrsDNTyiWQdSXyt8/giphy.gif",
            "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDdidmpkZGdnZWlucDkzOTUxMTBuY2swenBscndvaGs5eXluZ3kxdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/f6v1HAqfj2svgGAqh9/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjVtOXFqc3F4MGpqMTRncGNjZG4zaG44czc2cjBtOGpnMmYwb2txOSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/TGMxaNizlhAO8ykcR6/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjVtOXFqc3F4MGpqMTRncGNjZG4zaG44czc2cjBtOGpnMmYwb2txOSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/FmCK0RLDD4bHw7b01c/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjVtOXFqc3F4MGpqMTRncGNjZG4zaG44czc2cjBtOGpnMmYwb2txOSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/Fr2UB3zizQSNWzCy52/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/kKtAJrJUQnuikFZr3c/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/1HuE5ySqtdw2DNld57/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/fSEoD7tXf6esHkpwpN/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/hbVymgf2droIAXZr1d/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/B0LANRRToWzt12L0l7/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/zm0Cn3mSCGmGqC0aq8/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGluMmlyZzlzZm42YW1sNGo5NGl5NjJoMm5kd3FmMm44d2RrMzd4MSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/kKtAJrJUQnuikFZr3c/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OW5oMW5jeHVqd3I5d3Azemt4eXgxZDByZnUyMTc2d3g0aXQ0a29mMyZlcD12MV9zdGlja2Vyc19yZWxhdGVkJmN0PXM/NAnsmYj5gYBgWAgKvm/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OW5oMW5jeHVqd3I5d3Azemt4eXgxZDByZnUyMTc2d3g0aXQ0a29mMyZlcD12MV9zdGlja2Vyc19yZWxhdGVkJmN0PXM/M79tPFEkQkKFFT7rtB/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2p6OWswa3YyY2lpN2I1ZDlvbHNkYXMzeGJ4ZTh2YTc2MmVkMjJrZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3IXzpFl4UG4M0YwBHX/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2p6OWswa3YyY2lpN2I1ZDlvbHNkYXMzeGJ4ZTh2YTc2MmVkMjJrZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EoHuUABsiGOJrbZsIJ/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NHh1dng2ejVkYWlhazV5Y251empqbjdkdTIyd3p2bzNtZndrbG41OCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/UxES0P0wADBV5Msx0X/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dmh3M3hwamU2Y2UwOHRqeWc2MHBzNHJsZGM3OTE5eXc2OWQwaHh6eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IeFB04H51Ntwtam8Y8/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dmh3M3hwamU2Y2UwOHRqeWc2MHBzNHJsZGM3OTE5eXc2OWQwaHh6eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/to1LgMnVf6axPNkEry/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3a3R2OXk4MTVmazRtM25senVxY3FjemY0M25kN2NzYzJ3engzczdpZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XBHZ6DR6JRbCV68tC4/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3a3R2OXk4MTVmazRtM25senVxY3FjemY0M25kN2NzYzJ3engzczdpZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XBHZ6DR6JRbCV68tC4/giphy.gif"
        ]
        
        await ctx.send(random.choice(momo_gifs))
    else:
        # This line must also be on its own line!
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

#  woof and meow 
@bot.command(name="meow")
async def meow(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "cute cat")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

@bot.command(name="woof")
async def woof(ctx):
    if check_permissions(ctx):
        await send_gif(ctx, "cute dog")
    else:
        await ctx.send("Please use #bot-commands for GIFs!", delete_after=5)

 # GIF & Character Commands Section
    embed.add_field(
        name="✨ Fun & GIFs",
        value="`?meow` - Send a cute cat GIF\n"
              "`?woof` - Send a cute dog GIF\n"
              "`?chii` - Chiikawa GIFs\n"
              "`?hachi` - Hachiware GIFs\n"
              "`?usagi` - Usagi GIFs\n"
              "`?momo` - Momonga GIFs",
        inline=False
    )       



@bot.command(name="rblx")
async def rblx(ctx, genre: str = "all", page: int = 1):
    if not check_permissions(ctx):
        await ctx.send("🚫 **Access Denied!**", delete_after=3)
        return


    all_games = {
        "all": {
            1: [
                ("🏡 Brookhaven 🏡RP", "337K", "4924144360"),
                ("🐾 Adopt Me!", "301K", "920587237"),
                ("🍀 Sailor Piece", "266K", "17240378036"),
                ("🏴‍☠️ Blox Fruits", "256K", "2753915549"),
                ("🧱 Kick a Lucky Block", "221K", "16532051662")
            ],
            2: [
                ("🦊 99 Nights in the Forest", "153K", "1742398516"),
                ("🎯 RIVALS", "145K", "17625359962"),
                ("🐷 Steal a Brainrot", "145K", "17513224098"),
                ("🔪 Murder Mystery 2", "131K", "142823291"),
                ("🎣 Fish It! 👁️", "115K", "16823945172")
            ],
            3: [
                ("🟡 Jujutsu Shenanigans", "111K", "15376909623"),
                ("🫠 Slime RNG", "105K", "1782394519"),
                ("🪴 Grow a Garden 🌶️", "72K", "1672394518"),
                ("⚔️ Attack on Titan Rev", "67K", "14216969512"),
                ("🎲 Sol's RNG", "61K", "15532592331")
            ],
            4: [
                ("🐶 Pet Simulator 99!", "59K", "13155516556"),
                ("🥊 Strongest Battlegrounds", "59K", "10403348123"),
                ("👗 Catalog Avatar Creator", "54K", "7041939546"),
                ("🎣 Fisch 🎣", "47K", "16350361288"),
                ("🍓 Dandy's World [ALPHA]", "46K", "1623945172")
            ],
            5: [
                ("🌌 A Universal Time", "45K", "15165151"),
                ("🤺 Murderers VS Sheriffs", "43K", "15165151"),
                ("👹 Forsaken", "43K", "15165151"),
                ("🧟 Survive Zombie Arena", "41K", "15165151"),
                ("🚔 Jailbreak", "12K", "606849621")
            ]
        },
        "horror": {
            1: [
                ("🔪 Murder Mystery 2", "131K", "142823291"),
                ("🐝 Evade", "32K", "9872472334"),
                ("🔨 Flee the Facility", "12K", "893973440"),
                ("😱 3008 [2.74]", "11K", "2768379856"),
                ("🗣️ Escape Running Head", "5.5K", "10557454261")
            ],
            2: [
                ("⚔️ Survive the Killer!", "5.4K", "3901615617"),
                ("👤 SIREN HEAD: LEGACY", "5K", "5012586735"),
                ("🏮 PETAPETA | 0.1.2", "5K", "12255712175"),
                ("🐷 Piggy", "3.9K", "4623386818"),
                ("😱 Infectious Smile", "3.8K", "5112101672")
            ],
            3: [
                ("🌈 Rainbow Friends", "3.8K", "7991339063"),
                ("👵🏻️ Granny: Multiplayer", "3.4K", "121415151"),
                ("👹 Ophelia [HORROR]", "2.5K", "15478497672"),
                ("🔪 Secret Killer", "2.2K", "23385151"),
                ("🍕 FNAF: Eternal Nights", "2.2K", "12616541331")
            ],
            4: [
                ("👺 The Mimic", "2.1K", "6091722432"),
                ("🦴 SCP Monsters", "1.8K", "15165151"),
                ("💥 BUCKSHOT", "1.8K", "16516515"),
                ("🕷️ Spider", "1.5K", "4940101614"),
                ("🎁 Death in the Box", "1.5K", "13764749405")
            ],
            5: [
                ("🧸 Teddy", "1.3K", "4932130541"),
                ("💀 SCP Games", "1.3K", "15165151"),
                ("🦷 GEF", "1.2K", "13764749405"),
                ("👣 Apeirophobia", "6K", "10303102434"),
                ("🌑 Blackout", "300", "15165151")
            ]
        },
        "comedy": {
            1: [("🤝 Fling Things and People", "27K", "3181083910"), ("🍎 Secret Staycation", "6.4K", "14731393664"), ("👦 Silly Simon Says", "2.5K", "11852391060"), ("📊 The Presentation Exp", "1.5K", "6516541331"), ("🤡 DON'T GET ELIMINATED", "1.2K", "15165151")],
            2: [("♨️ NEOHEE HOT SPRING", "1.1K", "15165151"), ("🐈 BAD CAT", "1.1K", "15165151"), ("💥 Horrific Housing", "889", "15165151"), ("🍰 Half A Slice Of Cake", "753", "15165151"), ("🦴 Broken Bones IV", "612", "15165151")],
            3: [("🔧 random tool", "574", "15165151"), ("🥔 PLAY OR DIE", "503", "15165151"), ("🤸 Ragdoll Physics Havoc", "469", "15165151"), ("🐝 Spelling Bee", "409", "15165151"), ("💣 Pass the Bomb!", "384", "15165151")],
            4: [("🌊 Ragdoll Waterpark", "373", "15165151"), ("🍌 Banana Nextbot", "372", "15165151"), ("🏃 Dynamic Ragdoll Engine", "371", "15165151"), ("🕳️ Hole in the Wall", "358", "15165151"), ("👗 Outfit Loader", "294", "15165151")],
            5: [("🤣 Crazy Cards", "246", "15165151"), ("✋ GODS WILL", "187", "15165151"), ("🌱 Grass Cutting Inc", "182", "15165151"), ("✍️ Copyrighted Artists", "173", "15165151"), ("🚌 Bus Simulator", "2K", "11652391060")]
        }, "fps": {
            1: [("🎯 RIVALS", "145K", "17625359962"), ("🔥 Hype", "16K", "15165151"), ("⚔️ Combat Arena", "4K", "15165151"), ("🎖️ Phantom Forces", "1.9K", "292439477"), ("💰 Notoriety", "1.4K", "15165151")],
            2: [("🧟 Reminiscence Zombies", "919", "15165151"), ("🔫 Typical Colors 2", "753", "328028363"), ("🌲 Fallen Survival", "707", "15165151"), ("💀 Project Lazarus", "699", "443406476"), ("🛡️ Gun and Armor Testing", "544", "15165151")],
            3: [("🎖️ Dogs of War", "475", "15165151"), ("🧟 Michael's Zombies", "425", "15165151"), ("🏡 town", "422", "15165151"), ("💣 Counter Blox", "410", "301549746"), ("🎨 BIG Paintball 2!", "378", "15165151")],
            4: [("🔫 Weaponry [BETA]", "353", "15165151"), ("✈️ Airship Assault", "351", "15165151"), ("🧱 Ray's Mod", "306", "15165151"), ("🔫 Airsoft FE", "288", "15165151"), ("💀 Glory Kill Testing", "283", "15165151")],
            5: [("🔫 Gun Grounds FFA", "280", "15165151"), ("❄️ Decaying Winter", "261", "15165151"), ("🧟 Korrupt Zombies", "260", "15165151"), ("⚡ Energy Assault FPS", "244", "15165151"), ("🎖️ Military Sim", "1K", "23385151")]
        },
        "adventure": {
            1: [
                ("🏴‍☠️ Blox Fruits", "256K", "2753915549"),
                ("⚔️ Attack on Titan Rev", "67K", "14216969512"),
                ("🎣 Fisch 🎣", "47K", "16350361288"),
                ("🐝 Bee Swarm Simulator", "27K", "15376909623"),
                ("🏎️ Driving Empire", "17K", "335165151")
            ],
            2: [
                ("👮 BARRY'S PRISON RUN", "11K", "10557454261"),
                ("⛵ Build A Boat For Treasure", "9.8K", "537413528"),
                ("🐉 Dragon Adventures", "9.3K", "3475397644"),
                ("👑 King Legacy", "7.7K", "4520749081"),
                ("🦑 Squid Game X", "7.4K", "7540891731")
            ],
            3: [
                ("👁️ DOORS", "5.5K", "6516141723"),
                ("🚘 Collector! Car Dealership", "5.4K", "15165151"),
                ("🚜 Off-Roading Epic", "5.4K", "15165151"),
                ("🏫 Team School Breakout!", "5K", "15165151"),
                ("🤡 Insane Elevator!", "4.9K", "15165151")
            ],
            4: [
                ("🚐 a dusty trip [📜QUESTS]", "4.8K", "16389395869"),
                ("🗼 Tower of Hell", "4.8K", "1962086868"),
                ("🌑 Abyssal 🟡", "4.5K", "15165151"),
                ("🐘 Ecos: La Brea", "4K", "15165151"),
                ("🦔 Sonic Speed Simulator", "3.7K", "9049840490")
            ],
            5: [
                ("🚐 RV Cooked? [ALPHA]", "2.9K", "15165151"),
                ("🔮 Arcane Odyssey", "2.8K", "3272915504"),
                ("🎨 Color or Die 🎨", "2.5K", "13143580556"),
                ("🌊 Grand Piece Online", "2.4K", "1730877806"),
                ("🏔️ Expedition", "1.5K", "15165151")
            ]
        },
        "fighting": {
            1: [("👊 Jujutsu Shenanigans", "111K", "15376909623"), ("🥊 Strongest Battlegrounds", "59K", "10403348123"), ("🛌 BedWars", "11K", "6872265039"), ("⚔️ Blade Ball", "10K", "13772394625"), ("🤠 Murderers vs Sheriffs", "8.8K", "15165151")],
            2: [("🦸 Heroes Battlegrounds", "8.4K", "15165151"), ("🤺 ABA", "8.3K", "15165151"), ("🥊 untitled boxing game", "7.5K", "1362165151"), ("🥊 Boxing Beta", "6.6K", "15165151"), ("🔫 Murderers VS Sheriffs", "6.5K", "15165151")],
            3: [("🛡️ War Tycoon", "5.2K", "15165151"), ("👋 Slap Battles", "4.9K", "6403330168"), ("🏰 Build to Survive", "4.8K", "15165151"), ("🍓 Fruit Battlegrounds", "4.1K", "15165151"), ("⚡ Elemental Powers Tycoon", "3.8K", "15165151")],
            4: [("👻 TYPE://SOUL", "3.8K", "13143580556"), ("🐉 Dragon Ball RPG", "3K", "15165151"), ("🔫 Arsenal", "3K", "286090429"), ("💪 Muscle Legends", "2.9K", "3623096087"), ("🏰 Build to Survive ⚔️", "2.8K", "15165151")],
            5: [("🖋️ Bendy & Ink Machine", "2.6K", "15165151"), ("👹 A Universal Time", "2.6K", "15165151"), ("🧔 Dudes Battlegrounds", "2.5K", "15165151"), ("💥 Ultimate Battlegrounds", "2.2K", "15165151"), ("🤜 Tower Defense", "10K", "4996049426")]
        },
        "building": {
            1: [
                ("🎡 Theme Park Tycoon 2", "3.1K", "69184822"),
                ("🛠️ Plane Crazy", "2.8K", "2913303231"),
                ("🏭 Industrialist", "2.1K", "15165151"),
                ("🍳 Restaurant Tycoon 2", "1.6K", "185655149"),
                ("🏗️ Obby Creator", "1.6K", "2913303231")
            ],
            2: [
                ("🛒 Retail Tycoon 2", "1.4K", "410522069"),
                ("🗼 Infinite Tower Tycoon", "1.3K", "15165151"),
                ("🚧 construction", "1.1K", "15165151"),
                ("🐯 Zoo Tycoon", "1K", "15165151"),
                ("🌲 Oaklands", "981", "15165151")
            ],
            3: [
                ("👮 My Prison", "783", "15165151"),
                ("⚡ God's Mod", "765", "15165151"),
                ("🛡️ Colony Survival", "482", "15165151"),
                ("⚙️ Factory Simulator", "404", "15165151"),
                ("🎨 Draw & Donate", "363", "15165151")
            ],
            4: [
                ("📼 RetroStudio", "337", "15165151"),
                ("🧙 Wizard Tycoon", "210", "15165151"),
                ("🛳️ Cruise Line Tycoon", "174", "15165151"),
                ("⛏️ Miner's Haven", "171", "15165151"),
                ("⛵ Build A Boat With Blocks", "161", "15165151")
            ],
            5: [
                ("₿ Bitcoin Miner", "158", "15165151"),
                ("🔨 Tower Creator", "157", "15165151"),
                ("🖥️ Custom PC Tycoon!", "151", "15165151"),
                ("🏢 Jump Off A Building", "145", "15165151"),
                ("🏗️ Construction Sim", "2K", "15165151")
            ]
        },
        "obby": {
            1: [
                ("🗼 Tower of Hell", "4.7K", "1962086868"),
                ("👗 Would You Rather: Outfit", "13.7K", "15165151"),
                ("🚌 Dangerous Bus Driving", "761", "15165151"),
                ("⌨️ ASMR Keyboard Tower", "6.5K", "15165151"),
                ("🛹 Skateboard Obby", "563", "15165151")
            ],
            2: [
                ("🔗 Chained Together", "574", "15165151"),
                ("🥳 Together [Party Game]", "2.3K", "15165151"),
                ("🧟 Tower of Zombies", "2K", "15165151"),
                ("🐛 Climb Scary Worm", "2.4K", "15165151"),
                ("⛩️ Anime Tower", "1.1K", "15165151")
            ],
            3: [
                ("🌀 Parkour Spiral", "755", "15165151"),
                ("🎧 Phonk Edit Tower", "3K", "15165151"),
                ("👻 Climb Scary Pocong", "3.1K", "15165151"),
                ("🌈 oMega Obby 🌟", "1.2K", "15165151"),
                ("🚲 Bike of Hell", "766", "15165151")
            ]
        },
        "sports": {
            1: [("⚽ Football Fusion", "5K"), ("🏀 Basketball Legends", "8K"), ("🛹 Skate Park", "1K"), ("🏁 Driving Empire", "15K"), ("🏏 Cricket 24", "200")],
            2: [("🎾 Tennis Clash", "400"), ("🥊 Boxing League", "2K"), ("🏈 Gridiron", "1K"), ("🏐 Volleyball 4.0", "500"), ("⛳ Golf Sim", "300")],
            3: [("⛸️ Ice Skating", "100"), ("🥋 Martial Arts", "400"), ("🏹 Archery", "200"), ("🏃 Track & Field", "500"), ("🚵 MTB Downhill", "300")],
            4: [("🎿 Skiing", "50"), ("🌊 Surfing", "200"), ("🧗 Climbing", "400"), ("🎳 Bowling", "300"), ("🎱 Billiards", "150")],
            5: [("🏸 Badminton", "100"), ("🛶 Rowing", "50"), ("🏇 Horse Racing", "400"), ("🤺 Fencing", "100"), ("🧘 Yoga Sim", "50")]
        },
        "medieval": {
            1: [
                ("🌲 Foresto: Hunting", "353", "15165151"),
                ("🛡️ ARCHEMARA", "44", "15165151"),
                ("⚔️ Sword Fights", "23", "15165151"),
                ("🏰 Field of Battle", "15", "15165151"),
                ("🏯 Village Defense", "14", "15165151")
            ],
            2: [
                ("⚔️ Sword Clash", "1", "15165151"),
                ("🛡️ Warlords", "0", "15165151"),
                ("👑 Kingdom Life II", "0", "15165151"),
                ("🏰 Medieval Warfare", "400", "15165151"),
                ("🐉 Dragon Adventures", "8K", "3475397644")]
        },
        "military": {
            1: [("💂 Guts & Blackpowder", "5.9K", "12334142514"), ("🚁 Blackhawk Rescue 5", "3.2K", "2913303231"), ("🎖️ ENTRENCHED WW1", "2.9K", "4610282794"), ("🌍 Conquer The World", "2.6K", "15165151"), ("🎖️ Noob Army Tycoon", "2.5K", "15165151")],
            2: [("💀 Grave/Digger", "1.3K", "15165151"), ("✈️ RED VS BLUE PLANES", "1.1K", "15165151"), ("🚩 Rise of Nations", "820", "2571707014"), ("🎯 kill npcs or something", "779", "15165151"), ("📜 Lexington & Concord", "657", "15165151")],
            3: [("🚜 Cursed Tank Simulator", "403", "15165151"), ("🏹 Trench Combat", "252", "15165151"), ("🎖️ Noobs in Combat", "235", "15165151"), ("🛡️ Dummies vs Noobs", "232", "15165151"), ("✈️ Wings of Glory", "178", "15165151")],
            4: [("🎖️ War Simulator", "175", "15165151"), ("🚜 Tank Simulator", "141", "15165151"), ("🎖️ The Eastern War 2.5", "122", "15165151"), ("🔫 Special Forces Sim", "120", "15165151"), ("🏹 Trench War", "111", "15165151")],
            5: [("🚜 Steel Titans", "107", "15165151"), ("🎖️ D-DAY", "77", "15165151"), ("🏙️ State of Anarchy", "74", "15165151"), ("🎖️ Pordier at War", "72", "15165151"), ("🎖️ Army Sim", "1K", "23385151")]
        },
        "naval": {
            1: [("⚓ Harbor Havoc", "2.3K", "15165151"), ("🚢 Naval Warfare", "680", "23385151"), ("📦 Shipping Lanes", "442", "15165151"), ("🌊 Water Physics", "348", "15165151"), ("🎖️ DEAD AHEAD", "179", "15165151")],
            2: [("⛵ Tiny Sailor's WORLD", "106", "15165151"), ("⚓ Navy Simulator", "61", "15165151"), ("🚢 Dynamic Ship Sim", "38", "15165151"), ("⛵ Windward", "13", "15165151"), ("🏴‍☠️ Pirate Wars!", "13", "15165151")],
            3: [("🛳️ Battleship Tycoon", "0", "15165151"), ("🚢 Titanic", "1K", "23385151"), ("⛵ SharkBite 2", "4K", "23385151"), ("⚓ Harbor Tycoon", "200", "23385151"), ("🌊 Ships", "500", "23385151")],
            4: [("🛳️ Carrier", "500", "15165151"), ("🛶 Raft", "150", "15165151"), ("⚓ Coast Guard", "100", "15165151"), ("🌊 Deep Sea", "300", "15165151"), ("🛳️ Cruise", "1K", "15165151")],
            5: [("⛵ Sailing", "200", "15165151"), ("⚓ Port Builder", "300", "15165151"), ("🌊 Waves", "100", "15165151"), ("🛶 Rowing", "50", "15165151"), ("🚢 Ship Tycoon", "1K", "15165151")]
        },
        "rpg": {
            1: [("🐾 Adopt Me!", "301K", "920587237"), ("📖 Block Tales", "12K", "15165151"), ("🌊 Deepwoken", "7.2K", "5735564870"), ("🍁 Maple Hospital", "6.7K", "15165151"), ("🍼 Twilight Daycare", "4.2K", "15165151")],
            2: [("📜 Archived", "2.8K", "15165151"), ("🐈 Warrior Cats", "1.9K", "15165151"), ("⚔️ World // Zero", "1.3K", "2727333891"), ("🛡️ SCP: Roleplay", "1.2K", "5041144496"), ("🍇 Pilgrammed", "964", "15165151")],
            3: [("🏹 Arcane Odyssey", "924", "3272915504"), ("🏡 Club Roblox RP", "917", "15165151"), ("⌚ Ben 10 Time", "899", "15165151"), ("🐺 Forgotten Worlds", "852", "15165151"), ("🍼 Parenthood Beta", "720", "15165151")],
            4: [("🤸 Ragdoll Physics", "641", "15165151"), ("🎭 Fantasia", "548", "15165151"), ("👿 Vesteria", "452", "15165151"), ("🎤 Trivia! Game Show", "443", "15165151"), ("🌸 Kaizen [RP]", "413", "15165151")],
            5: [("🧜 Mermaid Lagoon", "376", "15165151"), ("🧟 Zombie lab", "333", "15165151"), ("✨ Pulse RP", "248", "15165151"), ("🐎 Horse World", "245", "15165151"), ("🛡️ Hero Quest", "1K", "23385151")]
        },
        "scifi": {
            1: [("🛸 Impostor | Among us", "467", "15165151"), ("🚀 Space Sailors", "450", "15165151"), ("🛰️ Project Stardust", "174", "15165151"), ("🕳️ Black Hole Core", "172", "15165151"), ("🎮 Ready Player Two Hub", "120", "15165151")],
            2: [("👥 Clone Tycoon 2", "120", "15165151"), ("🦖 DARKDIVERS 0.6", "101", "15165151"), ("🚀 Innovation Spaceship", "98", "15165151"), ("🌌 STARBASIS", "93", "15165151"), ("🛰️ Space Station Infinity", "75", "15165151")],
            3: [("🌌 The Known Galaxy", "71", "15165151"), ("🪐 be a planet", "56", "15165151"), ("🛸 UFO Tycoon", "46", "15165151"), ("🦀 Crab Lab", "31", "15165151"), ("☢️ Pinewood Computer", "26", "15165151")],
            4: [("🚀 Space Wars", "22", "15165151"), ("🎖️ Eras of War", "21", "15165151"), ("🚀 Rocket Tester", "21", "15165151"), ("🌌 Starscape [Beta]", "19", "15165151"), ("☢️ QS Energy Research", "18", "15165151")],
            5: [("⚡ Thermal Power Plant", "17", "15165151"), ("🐱 Transfur Outbreak", "12", "15165151"), ("🛰️ Death Star Tycoon", "12", "15165151"), ("⚡ The Flash", "11", "15165151"), ("🚀 Galaxy", "1K", "15165151")]
        },
        "sports": {
            1: [("⚽ Realistic Street Soccer", "4.7K", "15165151"), ("⚽ FIFA Super Soccer!", "4K", "15165151"), ("🏀 Basketball Legends", "3.3K", "15165151"), ("🏈 NFL Universe Football", "2.8K", "15165151"), ("🏈 Football Fusion 2", "1.6K", "15165151")],
            2: [("⚽ Soccer: Touch Football", "800", "15165151"), ("⚽ Team Soccer", "720", "15165151"), ("🏎️ Formula Apex Racing", "642", "15165151"), ("🏃 Track & Field: Infinite", "544", "15165151"), ("⚽ Goal Kick Sim", "419", "15165151")],
            3: [("🎱 8-Pool Pool Classic", "417", "15165151"), ("🏎️ Backstretch Battles", "406", "15165151"), ("⛳ Super Golf!", "395", "15165151"), ("⚽ TPS: Street Soccer", "367", "15165151"), ("⚽ Touch Soccer", "365", "15165151")],
            4: [("🏎️ just daytona", "363", "15165151"), ("⛳ Golf Frenzy!", "321", "15165151"), ("⚾ HCBB 9v9 2.0", "310", "15165151"), ("🏀 Hoop Nation", "301", "15165151"), ("🏀 Basketball Stars 3", "298", "15165151")],
            5: [("🏀 Highschool Hoops", "271", "15165151"), ("⚽ The Classic Soccer", "260", "15165151"), ("🏐 Volleyball 4.2", "259", "15165151"), ("⚽ Goal Battles", "237", "15165151"), ("🥊 Boxing League", "2K", "15165151")]
        },
        "townandcity": {
            1: [("🏡 Brookhaven 🏡RP", "337K", "4924144360"), ("🏗️ Welcome to Bloxburg", "14K", "185655149"), ("📱 LifeTogether 🏠 RP", "14K", "15165151"), ("💅 Berry Avenue 💅 RP", "12K", "12543361585"), ("🏙️ Metro Life 🏠 City RP", "12K", "15165151")],
            2: [("🏠 Livetopia 🏠 RP", "8.2K", "5733315553"), ("💃 Salon de Fiestas", "8K", "15165151"), ("🚔 Prison Life", "7.4K", "15165151"), ("🏎️ Midnight Chasers", "6.3K", "15165151"), ("✨ Gacha Online", "5.9K", "15165151")],
            3: [("✈️ NewSmith 🏠 RP", "5.3K", "15165151"), ("🚗 Car Driving Indonesia", "5K", "15165151"), ("🚔 Jailbreak", "4.8K", "606849621"), ("🚕 Taxi Boss 🚕", "4.7K", "15165151"), ("🐰 Neighbors 🔊", "4.1K", "15165151")],
            4: [("🚔 Emergency Response", "3.9K", "15165151"), ("🍕 Work at a Pizza Place", "3.7K", "192800"), ("🏎️ Roanoke, VA", "3.6K", "15165151"), ("🚔 Wanted", "3.1K", "15165151"), ("🎰 Bloxy Bingo", "3.1K", "15165151")],
            5: [("🏙️ Redcliff City 🏡RP", "3K", "15165151"), ("🚗 Greenville", "3K", "15165151"), ("🐰 Neighbors [18+]", "2.7K", "15165151"), ("🚔 Emergency Hamburg", "2.3K", "15165151"), ("🏙️ MeepCity", "10K", "370731277")]
        },
        "western": {
            1: [
                ("🤠 NPC or DIE!", "2.4K", "15165151"),
                ("🔫 Westbound", "772", "23385151"),
                ("🐎 The Wild West", "549", "2317712696"),
                ("💎 The Quarry", "1", "15165151"),
                ("🎸 Lil Nas X Concert", "0", "15165151")
            ],
            2: [
                ("🐎 Horse Life", "3K", "15165151"),
                ("🚂 Train Tycoon", "200", "15165151"),
                ("🌵 Desert Obby", "100", "15165151"),
                ("🤠 Cowboy Tycoon", "500", "15165151"),
                ("🔫 Wild West Duel", "300", "15165151")]
      }
}

    if genre.lower() == "genres":
        genres_list = list(all_games.keys())
        # Format the list nicely with emojis
        formatted_list = "\n".join([f"• `{g.capitalize()}`" for g in genres_list])
        
        embed = discord.Embed(
            title="📂 Available Roblox Categories",
            description=f"Use `?rblx [genre]` to browse top games!\n\n{formatted_list}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Tip: You can also add a page number, like '?rblx horror 2'")
        await ctx.send(embed=embed)
        return
    

    clean_genre = genre.lower().replace(" ", "")
    if "all" in clean_genre: clean_genre = "all"
    
    genre_data = all_games.get(clean_genre, all_games["all"])
    page = max(1, min(page, 5))
    results = genre_data.get(page, genre_data[1])

    embed = discord.Embed(
        title=f"🫰🏻 {genre.upper()} | PAGE {page} 🫰🏻 (DATA FROM ROLIMONS.COM)",
        color=discord.Color.from_rgb(255, 69, 0)
    )

    for name, players, place_id in results:
        direct_link = f"https://www.roblox.com/games/{place_id}"
        embed.add_field(
            name=f"🎮 {name}",
            value=f"👤 **{players}** | [**PLAY NOW**]({direct_link})",
            inline=False
        )

    if page < 5:
        next_page = page + 1
    else:
        next_page = 1

    embed.set_footer(text=f"page {page}/5 - Use '?rblx {genre} {next_page} for more games' • Tuffest sigma alpha bot")
    await ctx.send(embed=embed)





@bot.command(name="coms")
async def coms(ctx):
    if not check_permissions(ctx):
        await ctx.send("🚫 **Access Denied!**", delete_after=3)
        return

    embed = discord.Embed(
        title="🤖 Bot Commands List",
        description="Here are all the available commands you can use!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="🎮 Roblox Games",
        value="`?rblx` — Shows top trending games\n"
              "`?rblx genres` — List categories\n"
              "`?rblx [genre] [page]` — Browse games",
        inline=False
    )

    embed.add_field(
        name="💰 Economy & Gambling",
        value="`?daily` — Claim your daily Meowency\n"
              "`?bal` — Check your vault balance\n"
              "`?coin [heads/tails] [bet]` — High stakes coinflip flip\n"
              "`?slots [bet]` — Animated cyber slots\n"
              "`?dice [bet] [1-6]` — Roll the lucky cat dice\n"
              "`?bj [bet]` - Play blackjack\n"
              "`?top` — View the best gamblers",
        inline=False
    )

    embed.add_field(
        name="✨ Fun & GIFs",
        value="`?meow`, `?woof` — Animal GIFs\n"
              "`?chii`, `?hachi`, `?usagi`, `?momo` — Chiikawa GIFS\n"
              "`?deltarune`, `?kris`, `?susie`, `?ralsei` — Deltarune GIFS",
        inline=False
    )

    embed.set_footer(text=f"Requested by {ctx.author.name} • Bot by tuff sigma alpha wolf")
    await ctx.send(embed=embed)


@bot.command(name="daily")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    vault = load_vault()
    uid = str(ctx.author.id)
    
    reward = random.randint(500, 1500) 
    vault[uid] = vault.get(uid, 0) + reward
    save_vault(vault)

    embed = discord.Embed(
        title="🐾 MEOWENCY DELIVERY!",
        description=f"You claimed your daily allowance of **{reward} meowency**!",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total Balance: {vault[uid]:,}")
    await ctx.send(embed=embed)


        
@bot.command(name="coin")
@commands.cooldown(1, 7, commands.BucketType.user) # 1 use every 7 seconds
async def coin(ctx, choice: str, bet: int):
    vault = load_vault()
    uid = str(ctx.author.id)
    balance = vault.get(uid, 0)

    valid_choices = ["tails", "heads"]
    user_choice = choice.lower()

    if user_choice not in valid_choices:
        return await ctx.send("❌ You must choose either **tails** or **heads**!")
    
    if bet < 100:
        return await ctx.send("❌ The minimum bet is **100 meowency**!")
    
    if bet > balance:
        return await ctx.send(f"❌ You don't have enough meowency! Balance: {balance:,}")

    winning_side = random.choice(valid_choices)
    
    if user_choice == winning_side:
        vault[uid] = balance + bet
        result_msg = f"✨ **{winning_side.upper()}!** You guessed right and won **{bet} meowency**!"
        color = discord.Color.green()
    else:
        vault[uid] = balance - bet
        result_msg = f"💀 **{winning_side.upper()}...** Wrong choice. You lost **{bet} meowency**."
        color = discord.Color.red()

    save_vault(vault)

    embed = discord.Embed(title=" The Coinflip Flip", description=result_msg, color=color)
    embed.set_footer(text=f"New Balance: {vault[uid]:,}")
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 7, commands.BucketType.user)
async def slots(ctx, bet: int):
    vault = load_vault()
    uid = str(ctx.author.id)
    balance = vault.get(uid, 0)
    
    if bet > balance or bet < 100:
        return await ctx.send(f"❌ Min bet is **100 meowency**! Your balance: **{balance:,}**")

    items = ["🐱", "🐾", "🐟", "🧶", "💀", "💩", "💩", "💀", "💩", "💀"]
    res = [random.choice(items) for _ in range(3)]
    
    header = f"** `___SLOTS___`**\n"
    
    msg = await ctx.send(f"{header}` ` 🔄 🔄 🔄 ` ` *Spinning...*")
    await asyncio.sleep(1)

    # 2. DETERMINE WINNINGS
    if res[0] == res[1] == res[2]:
        payout = bet * 15
        status = f"and **WON {payout:,}!!** ✨"
    elif res[0] == res[1] or res[1] == res[2] or res[0] == res[2]:
        payout = bet * 2
        status = f"and won {payout:,}! :3"
    else:
        payout = -bet
        status = f"and won nothing... :c"

    vault[uid] = balance + payout
    save_vault(vault)

    final_view = (
        f"{header}"
        f"` ` {res[0]} {res[1]} {res[2]} ` `  ({ctx.author.display_name}) bet 🐾 {bet:,}\n"
        f"  `|         |`   {status}\n"
        f"  `|         |`   **Balance:** {vault[uid]:,} 🐾"
    )
    
    await msg.edit(content=final_view)

@bot.command(name="dice")
@commands.cooldown(1, 7, commands.BucketType.user)
async def dice_gamble(ctx, bet: int, guess: int):
    vault = load_vault()
    uid = str(ctx.author.id)
    balance = vault.get(uid, 0)
    
    if guess < 1 or guess > 6:
        return await ctx.send("🎲 **Invalid Guess!** Please pick a number between **1 and 6**.")
    
    if bet < 100:
        return await ctx.send("❌ The minimum bet is **100 meowency**!")
    
    if bet > balance:
        return await ctx.send(f"❌ You don't have enough meowency! Balance: {balance:,}")

    bot_roll = random.randint(1, 6)
    
    dice_faces = {1: "💸", 2: "💸", 3: "💸", 4: "💸", 5: "💸", 6: "💸"}
    
    if guess == bot_roll:
        payout = bet * 4
        vault[uid] = balance + payout
        result_msg = f"✨ **LUCKY ROLL!**\nThe dice landed on {dice_faces[bot_roll]} **({bot_roll})**.\nSuccessfully added **{payout:,} meowency** to your wallet!"
        color = discord.Color.green()
    else:
        vault[uid] = balance - bet
        result_msg = f"💀 **Bummer!**\nThe dice landed on {dice_faces[bot_roll]} **({bot_roll})**.\nYou guessed **{guess}**. You lost your bet."
        color = discord.Color.red()

    save_vault(vault)

    embed = discord.Embed(title="🎲 High-Stakes Dice Roll", description=result_msg, color=color)
    # The balance is clearly shown at the end here
    embed.set_footer(text=f"New Balance: {vault[uid]:,} Meowency")
    await ctx.send(embed=embed)

    

def get_card():
    cards = [
        ('2', '2️⃣'), ('3', '3️⃣'), ('4', '4️⃣'), ('5', '5️⃣'), ('6', '6️⃣'), 
        ('7', '7️⃣'), ('8', '8️⃣'), ('9', '9️⃣'), ('10', '🔟'), 
        ('J', '🤴'), ('Q', '👸'), ('K', '🤡'), ('A', '🅰️')
    ]
    return random.choice(cards)

def calculate_hand(hand):
    value = 0
    aces = 0
    for card_val, emoji in hand:
        if card_val in ['J', 'Q', 'K']: value += 10
        elif card_val == 'A': aces += 1
        else: value += int(card_val)
    
    for _ in range(aces):
        if value + 11 <= 21: value += 11
        else: value += 1
    return value
class BlackjackView(discord.ui.View):
    def __init__(self, ctx, bet, player_hand, dealer_hand):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bet = bet
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    async def update_embed(self, interaction, final=False):
        p_val = calculate_hand(self.player_hand)
        d_val = calculate_hand(self.dealer_hand)
        
        embed = discord.Embed(title="🃏 Blackjack Table", color=discord.Color.dark_grey())
        embed.description = f"👤 **{self.ctx.author.display_name}**, you bet **{self.bet:,} meowency**"
        
        d_label = f"Dealer [{d_val}]" if final else "Dealer [?]"
        d_cards = " ".join([c[1] for c in self.dealer_hand]) if final else f"{self.dealer_hand[0][1]} 🎴"
        
        p_label = f"{self.ctx.author.display_name} [{p_val}]"
        p_cards = " ".join([c[1] for c in self.player_hand])
        
        embed.add_field(name=d_label, value=d_cards, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) # Spacer
        embed.add_field(name=p_label, value=p_cards, inline=True)
        
        if final:
            self.stop()
            vault = load_vault()
            uid = str(self.ctx.author.id)
            user_bal = vault.get(uid, 0)
            
            if p_val > 21:
                res, color, change = "❌ BUSTED! You lost.", discord.Color.red(), -self.bet
            elif d_val > 21 or p_val > d_val:
                res, color, change = f"✨ YOU WIN! Added {self.bet:,} meowency.", discord.Color.green(), self.bet
            elif p_val < d_val:
                res, color, change = "💀 Dealer wins.", discord.Color.red(), -self.bet
            else:
                res, color, change = "🤝 IT'S A TIE (Push).", discord.Color.gold(), 0
            
            new_bal = user_bal + change
            vault[uid] = max(0, new_bal) # Ensure balance never goes below 0
            save_vault(vault)
            
            embed.color = color
            embed.add_field(name="🏁 Result", value=f"```\n{res}\n```", inline=False)
            
            embed.set_footer(text=f"New Balance: {vault[uid]:,} Meowency")
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.success, emoji="👊")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        self.player_hand.append(get_card())
        if calculate_hand(self.player_hand) >= 21:
            await self.update_embed(interaction, final=True)
        else:
            await self.update_embed(interaction)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.danger, emoji="🛑")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author: return
        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(get_card())
        await self.update_embed(interaction, final=True)

@bot.command(name="bj")
@commands.cooldown(1, 10, commands.BucketType.user)
async def blackjack(ctx, bet: int):
    vault = load_vault()
    uid = str(ctx.author.id)
    if vault.get(uid, 0) < bet or bet < 100:
        return await ctx.send("❌ Minimum bet is 100 and you need enough meowency!")

    player_hand = [get_card(), get_card()]
    dealer_hand = [get_card(), get_card()]
    
    view = BlackjackView(ctx, bet, player_hand, dealer_hand)
    embed = discord.Embed(title="🃏 Blackjack Table", color=discord.Color.dark_grey())
    embed.description = f"👤 **{ctx.author.display_name}**, you bet **{bet:,} meowency**"
    embed.add_field(name="Dealer [?]", value=f"{dealer_hand[0][1]} 🎴", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name=f"{ctx.author.display_name} [{calculate_hand(player_hand)}]", 
                    value=" ".join([c[1] for c in player_hand]), inline=True)
    
    await ctx.send(embed=embed, view=view)
     
@bot.command(name="moneh")
async def moneh_command(ctx, amount: int, member: discord.Member):
    if ctx.author.id == 778891631591686164:
        vault = load_vault()
        uid = str(member.id)
        
        current_bal = vault.get(uid, 0)
        
        new_bal = current_bal + amount
        
        if new_bal < 0:
            new_bal = 0
            
        vault[uid] = new_bal
        save_vault(vault)

        if amount > 0:
            title = "🤑 MEOWENCY ADDED"
            color = discord.Color.green()
            action_text = f"Successfully added **{amount:,}**"
        else:
            title = "💩 MEOWENCY REMOVED"
            color = discord.Color.red()
            # abs() turns -100 into 100 for the message text
            action_text = f"Successfully removed **{abs(amount):,}**"

        embed = discord.Embed(
            title=title,
            description=f"{action_text} meowency from {member.mention}'s wallet 🤑.",
            color=color
        )
        embed.set_footer(text=f"Done by tuffest sigma alpha wolf • New Balance: {new_bal:,}")
        await ctx.send(embed=embed)
    
    else:
        await ctx.send("haha poop your pants 🫪🤑")


    
@bot.command()
async def bal(ctx):
    vault = load_vault()
    uid = str(ctx.author.id)
    balance = vault.get(uid, 0)
    await ctx.send(f"💰 **{ctx.author.display_name}**, you have **{balance} Meowency** in your wallet.")


@bot.command(name="top")
async def leaderboard(ctx):
    try:
        vault = load_vault()
        server_rankings = []

        async for member in ctx.guild.fetch_members(limit=None):
            uid_str = str(member.id)
            if uid_str in vault:
                server_rankings.append((member, vault[uid_str]))
        
        server_rankings.sort(key=lambda x: x[1], reverse=True)
        
        uid = str(ctx.author.id)
        user_rank = "N/A"
        for index, (member, balance) in enumerate(server_rankings, 1):
            if str(member.id) == uid:
                user_rank = index
                break

        embed = discord.Embed(
            title="🏆 MEOWENCY RANKINGS",
            color=discord.Color.gold()
        )
        
        personal_info = f"**💵 Your Rank**\nYou are rank `#{user_rank}` in this server\nwith a total of `{vault.get(uid, 0):,}` **Meowency**\n"
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        lb_list = ""
        for i, (member, balance) in enumerate(server_rankings[:10], 1):
            lb_list += f"**#{i}** {member.mention} **{member.name}** • 🐾 `{balance:,}`\n"

        embed.description = f"{personal_info}\n**GLOBAL USERNAMES**\n{lb_list if lb_list else 'No members found!'}"
        
        embed.set_footer(text=f"Page 1 of 1 • Requested by {ctx.author.display_name}")

        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Leaderboard Error: {e}")
        await ctx.send("❌ Something went wrong. Check the bot terminal.")
        
async def send_gif(ctx, search_term):
    
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={search_term}&limit=50&rating=g"
    
    response = requests.get(url).json()
    
    if "data" in response and len(response["data"]) > 0:
        choice = random.choice(response["data"])
        gif_url = choice['images']['original']['url']
        await ctx.send(gif_url)
    else:
        await ctx.send(f"I couldn't find any GIFs for '{search_term}'.")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        finish_time = int(time.time() + error.retry_after)
        
        # Format <t:TIMESTAMP:R> creates the live countdown
        await ctx.send(f"⏳ **Too fast!** Please wait <t:{finish_time}:R> before using that again.")
        

bot.run(DISCORD_TOKEN)
