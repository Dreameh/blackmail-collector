import os, sys, argparse, secrets, discord
from dotenv import load_dotenv
from utils.database import Database
from discord.ext import commands as cmd
from discord.ext.commands import Bot
from datetime import datetime
import secrets


version = "0.0.1"

intents = discord.Intents.default()
intents.members = True
bot = Bot(intents=intents, command_prefix="!")
bot.remove_command('help')
db = Database()

@bot.event
async def on_ready():
    game = discord.Game("Collection all the good blackmail")
    print("Connected to discord.")
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.event
async def on_command_error(context, error):
    if isinstance(error, cmd.CommandNotFound):
        await context.send("{}, try !help for available commands.".format(error))

# Ping
@bot.command(pass_context=True)
async def ping(context):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    await context.send("Ping has been sent: {time}\n Latency: {latency}ms".format(time=current_time, latency=round(bot.latency * 1000)))
    print("Ping sent: " + current_time)

# Help
@bot.command(pass_context=True)
async def help(context):
    embed = discord.Embed(name="help")
    embed.set_author(name="Blackmail Collector Commands:")
    embed.add_field(name="To add blackmail:", value='!blackmail \"message\" @[user]', inline=False)
    embed.add_field(name="Send blackmail:", value="!sendblackmail @[user] @[id]", inline=False)
    embed.add_field(name="To display blackmail:", value="!getblackmail @[id]", inline=False)
    embed.add_field(name="Display random blackmail material from a random blackmailer", value="!random", inline=False)
    await context.send(embed=embed)

@bot.command(pass_context=True)
async def blackmail(context, message: str, user: discord.User):
    ID = secrets.token_hex(4)
    blackmail = (ID, context.author.id, message, user.id)
    if db.add(blackmail) is True:
        embed=discord.Embed(
            title = "New blackmail has been added",
            colour= discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        embed.add_field(name="ID", value=ID, inline=True)
        embed.add_field(name="Said by", value=user.display_name, inline=True)
        embed.add_field(name="Quote", value=message, inline=False)
        await context.send(embed=embed)
    else:
        await context.send("Something went wrong")

@bot.command(pass_context=True, name="get")
async def get_blackmail(context, ID):
    blackmail = db.get_one(ID)
    if blackmail is None:
        await context.send("No blackmail with that ID: " + ID)
    else:
        print(blackmail)
        idStr = blackmail[0]
        owner = blackmail[1]
        message = blackmail[2]
        target = blackmail[3]
        embed=discord.Embed(
            title = "New blackmail has been added",
            colour= discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        embed.add_field(name="ID", value=idStr, inline=True)
        embed.add_field(name="Owner", value=(await discord.Guild.get_user(owner)), inline=True)
        embed.add_field(name="Said by", value=(await discord.Guild.get_user(target)), inline=True)
        embed.add_field(name="Quote", value=message, inline=False)
        await context.send(embed=embed)

def main():
    try:
        print("Loading the Blackmail Collector v.{}".format(version))
        load_dotenv()
        token = os.getenv('token_secret')
        bot.run(token)
    except Exception as e:
        print("Environment has not been set: <" + str(e) + ">.")

if __name__ == "__main__":
    main()
