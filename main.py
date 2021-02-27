import discord
import os
from datetime import datetime
from discord.ext import commands as cmd
from discord.ext.commands import Bot
from dotenv import load_dotenv
from cogs import blackmail
from utilities import migration

version = "0.0.2"

# Setup bot
intents = discord.Intents.default()
intents.members = True
bot = Bot(intents=intents, command_prefix="-")
bot.add_cog(blackmail.Blackmail(bot))


@bot.event
async def on_ready():
    game = discord.Game("Collection all the good blackmail")
    print("Connected to discord.")
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.event
async def on_command_error(context, error):
    if isinstance(error, cmd.CommandNotFound):
        await context.send("{}, try !help for available commands.".format(error))


@bot.command(pass_context=True)
async def ping(context):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
    await context.send("Ping has been sent: {time}\n Latency: {latency}ms".format(time=current_time,
                                                                                  latency=round(bot.latency * 1000)))
    print("Ping sent: " + current_time)


def main():
    try:
        print("Loading the Blackmail Collector v.{}".format(version))
        load_dotenv()
        token = os.getenv('token_secret')
        bot.run(token)
    except discord.PrivilegedIntentsRequired:
        print(
            "Privileged Intents are required to use this bot. "
            "Enable them through the Discord Developer Portal.")
    except discord.DiscordException as e:
        print(e)
    except Exception as e:
        print("Environment has not been set: <" + str(e) + ">.")


if __name__ == "__main__":
    migration.migrate()
    main()
