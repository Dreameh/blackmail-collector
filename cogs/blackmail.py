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
            embed.add_field(name="ID", value=message_id["id"], inline=True)
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
            if db.is_owner_of_blackmail(int(context.author.id), int(blackmail_id)):
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
            try:
                blackmail = db.query_db('select * from blackmail where id=?', [int(blackmail_id)], True)
                owner: discord.Member = context.guild.get_member(blackmail["owner"])
                target: discord.Member = context.guild.get_member(blackmail["said_by_user"])
            except Exception as e:
                print(e)
            embed = discord.Embed(
                title="Blackmail",
                colour=discord.Colour.blue())
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
            embed.add_field(name="ID", value=blackmail["id"], inline=True)
            embed.add_field(name="Owner", value=owner.display_name, inline=True)
            embed.add_field(name="Said by", value=target.display_name, inline=True)
            embed.add_field(name="Quote", value=blackmail["message"], inline=False)
            await context.send(embed=embed)
        else:
            await context.send("No blackmail with that ID: `" + blackmail_id + "`")

    @commands.command(
        name="owner-list",
        description="Get owner's list of blackmail",
        brief="get owner's lil ol list of blackmail"
    )
    async def get_all_owner_blackmail(self, context):
        desc = "This is the list of messages:\n"
        for blackmail in db.query_db('SELECT * FROM blackmail WHERE owner=? LIMIT 0,20', [context.author.id]):
            member = context.guild.get_member(blackmail['said_by_user'])
            desc += """
                        **ID: ** {}
                        **Said by: ** {}
                        {} \n
                        """.format(blackmail['id'], member.display_name, blackmail['message'])
        embed = discord.Embed(
            title="**List of blackmail**",
            description=desc,
            colour=discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        count = db.query_db("SELECT COUNT(*) FROM blackmail where owner=?", [context.author.id], True)
        embed.set_footer(text="Page 1/" + str(count_helper(count[0])))
        await context.send(embed=embed)

    @commands.command(
        name="target-list",
        description="Get target's list of blackmail",
        brief="get target's lil ol list of blackmail"
    )
    async def get_all_target_blackmail(self, context, member: discord.Member):
        desc = "This is the list of messages:\n"
        for blackmail in db.query_db('SELECT * FROM blackmail WHERE said_by_user=? LIMIT 0,20', [member.id]):
            owner = context.guild.get_member(int(blackmail['owner']))
            desc += """
                    **ID: ** {}
                    **Reported by: ** {}
                    {} \n
                    """.format(blackmail['id'], owner.display_name, blackmail['message'])
        embed = discord.Embed(
            title="**List of blackmail**",
            description=desc,
            colour=discord.Colour.blue())
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/737268917449261127.gif?v=1")
        count = db.query_db("SELECT COUNT(*) FROM blackmail where owner=?", [context.author.id], True)
        embed.set_footer(text="Page 1/" + str(count_helper(count[0])))
        await context.send(embed=embed)


def count_helper(count):
    if (count / 20) < 1:
        return 1
    else:
        return round(count / 20)
