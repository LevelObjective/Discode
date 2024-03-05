import os
import dotenv

try:  
   dotenv.load_dotenv('dev.env')
except KeyError: 
   print("dev.env not found")
   exit(1)
token = os.getenv('TOKEN')

print(token)

import disnake
from disnake.ext import commands


bot = commands.InteractionBot()


@bot.event
async def on_ready():
    print("The bot is ready!")

bot.load_extension("commands.redeem")
bot.load_extension("commands.generate")

bot.run(token)