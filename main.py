import discord
from discord.ext import commands
from itertools import cycle
import json
import utilities
import assets
from datetime import datetime
import colorama
from colorama import Fore
from tqdm import tqdm
start_date = datetime.utcnow()
start_date_pretty = start_date.strftime("%d/%m/%Y %H:%M:%S")
print (Fore.RED + f"started on {start_date_pretty}\n")

print(Fore.RED + "Setting intents...\n")
intents = discord.Intents.default()
intents.members=True
intents.messages=True
intents.guilds=True


bot = commands.Bot(command_prefix="kasa-", case_insensitive = True, intents = intents)
token = utilities.read_json(assets.json_path)

if __name__ == "__main__":
    for extension in tqdm(assets.extensions, desc = "Loading extensions", unit = "Ex"):
        bot.load_extension(extension)
    print (Fore.GREEN + "Loaded all extennsions!\n")


@bot.event
async def on_ready():
    print(Fore.LIGHTBLUE_EX + "Bot online and fully loaded.")






bot.run(token["token"])