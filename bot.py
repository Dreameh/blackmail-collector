import sqlite3 as sql
import discord
from discord.ext import commands as cmd
from discord.ext.commands import Bot
from datetime import datetime
import os, sys, argparse
from dotenv import load_dotenv

bot = cmd.Bot(command_prefix="!")
bot.remove_command('help')

def connect_to_db():
    # Load the DB or else create new DB and connect to it.
    db_connection = sql.connect("blackmail.db")
    db_connection.cursor().execute("CREATE TABLE IF NOT EXISTS blackmail(id TEXT primary key, user TEXT, message TEXT, said_by_user TEXT, date_added Date)")
    print("SQLite3 DB has been loaded, or initiated.")
    db_connection.commit()

@bot.event
async def on_ready():
    game = discord.Game("Collecting all the good blackmail")
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

@bot.command(pass_content=True)
async def blackmail(context, message: str):
    embed=discord.Embed(
        title = "New blackmail has been added",
        colour= discord.Colour.blue())
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
    embed.add_field(name="ID", value="1234", inline=True)
    embed.add_field(name="Said by", value="@TEST", inline=True)
    embed.add_field(name="Quote", value=message, inline=False)
    await context.send(embed=embed)

def main():
    try:
        load_dotenv()
        token = os.getenv('token_secret')
        connect_to_db()
        bot.run(token)
    except Exception as e:
        print("Environment has not been set: <" + str(e) + ">.")

if __name__ == "__main__":
    main()
