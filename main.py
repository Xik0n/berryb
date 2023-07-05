import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all()) #activity = disnake.Activity(name='на ваш /отзыв', type=disnake.ActivityType.watching)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")        
        
bot.run('OTkwMjIyNDU0NjA3NzE2Mzcy.GM97Rr.Wd1804iyt-LN1W6VrbJSsdgvepW40nvmQCrB7')