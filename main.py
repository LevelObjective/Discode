import os
import disnake
from disnake.ext import commands
token = os.environ['TOKEN']

bot = commands.InteractionBot()


@bot.event
async def on_ready():
    print("The bot is ready!")

bot.load_extension("commands.redeem")
bot.load_extension("commands.generate")

bot.run(token)