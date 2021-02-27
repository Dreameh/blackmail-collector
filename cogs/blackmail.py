import secrets
from sqlite3 import Error

import discord
from discord.ext import commands
from utilities import db


class Blackmail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="add",
        description="Ability to add a new blackmail to the owners "
                    "list of blackmail material",
        brief="Add new blackmail item"
    )
    async def blackmail(self, context, message: str, member: discord.Member):
        blackmail = (int(context.author.id), message, int(member.id))
        try:
            message_id = db.add(blackmail)
            embed = discord.Embed(
                title="New blackmail has been added",
                colour=discord.Colour.blue())
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
            embed.add_field(name="ID", value=message_id[0], inline=True)
            embed.add_field(name="Said by", value=member.display_name, inline=True)
            embed.add_field(name="Quote", value=message, inline=False)
            await context.send(embed=embed)
        except Error as e:
            print(e)
            await context.send("Something went wrong")

    @commands.command(
        name="delete",
        description="Delete a specific blackmail item, using a {blackmail_id}"
                    "Remember that only the owner can delete a blackmail item",
        brief="Delete a specific blackmail item"
    )
    async def delete_blackmail(self, context, blackmail_id: str):
        try:
            check_owner = db.is_owner_of_blackmail(int(context.author.id), int(blackmail_id))
            if check_owner:
                db.delete_one(int(blackmail_id))
                await context.send("Message has been successfully deleted.")
            else:
                await context.send("You are not the owner of this")
        except Error as e:
            print(e)

    @commands.command(
        name="get",
        description="Get specific blackmail item",
        brief="Get specific blackmail item"
    )
    async def get_blackmail(self, context, blackmail_id: str):
        if db.check_if_entry_exists(int(blackmail_id)):
            blackmail = db.get_one(int(blackmail_id))
            _id = blackmail[0]
            owner: discord.Member = context.guild.get_member(blackmail[1])
            message = blackmail[2]
            target: discord.Member = context.guild.get_member(blackmail[3])
            embed = discord.Embed(
                title="Blackmail",
                colour=discord.Colour.blue())
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
            embed.add_field(name="ID", value=blackmail_id, inline=True)
            embed.add_field(name="Owner", value=owner.display_name, inline=True)
            embed.add_field(name="Said by", value=target.display_name, inline=True)
            embed.add_field(name="Quote", value=message, inline=False)
            await context.send(embed=embed)
        else:
            await context.send("No blackmail with that ID: `" + blackmail_id + "`")

    @commands.command(
        name="owner-list",
        description="Get owner's list of blackmail",
        brief="get owner's lil ol list of blackmail"
    )
    async def get_all_owner_blackmail(self, context):
        blackmail_list = db.get_all_from_owner(context.author.id)
        amount = db.count_all_from_owner(context.author.id)
        desc = "This is the list of messages:\n"
        for w in blackmail_list:
            member = context.guild.get_member(w[3])
            desc += """
                    **ID: ** {}
                    **Said by: ** {}
                    {} \n
                    """.format(w[0], member.display_name, w[2])
        embed = discord.Embed(
            title="**List of blackmail**",
            description=desc,
            colour=discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        await context.send(embed=embed)

    @commands.command(
        name="target-list",
        description="Get target's list of blackmail",
        brief="get target's lil ol list of blackmail"
    )
    async def get_all_target_blackmail(self, context, member: discord.Member):
        blackmail_list = db.get_all_from_target(int(member.id))
        amount = db.count_all_from_target(int(member.id))
        desc = "This is the list of messages:\n"
        for w in blackmail_list:
            member = context.guild.get_member(w[1])
            desc += """
                    **ID: ** {}
                    **Reported by: ** {}
                    {} \n
                    """.format(w[0], member.display_name, w[2])
        embed = discord.Embed(
            title="**List of blackmail**",
            description=desc,
            colour=discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        await context.send(embed=embed)
