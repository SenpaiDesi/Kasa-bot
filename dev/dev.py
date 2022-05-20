import discord
from discord.ext import commands
import aiosqlite
import asyncio

from discord.ext.commands.errors import MissingPermissions

db = "./database.db"

class dev(commands.Cog):
    """Dev only commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='setup', hidden=True)
    @commands.is_owner()
    async def dbsetup(self, ctx):
        """Db setup and init."""
        db = await aiosqlite.connect("./database.db")
        msg = await ctx.send("Initialising....")
        await asyncio.sleep(2)
        await msg.edit(content = "Setting up log db (task 1/4)")
        try:
           await db.execute("CREATE TABLE IF NOT EXISTS moderationLogs (logid INTEGER PRIMARY KEY, guildid int, moderationLogTypes int, userid int, moduserid int, content varchar, duration VARCHAR)")
           await db.commit()
        except Exception as e:
            return msg.edit(content = f"FAILED TASK 1/3 because of \n{e}")
        await asyncio.sleep(2)
        await msg.edit(content = "Creating log type converter (task 2/4)")
        try:
            await db.execute("CREATE TABLE IF NOT EXISTS logtypes (Type INTEGER PRIMARY KEY, Form TEXT)")
            await db.commit()
        except Exception as e:
            return await msg.edit(content  = f"FAILED TASK 2/4 because of \n{e}")
        await asyncio.sleep(2)
        await msg.edit(content  = "Inserting default logtype converter (task 3/3)")
        try:
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (1, "warn",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (2, "mute",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (3, "unmute",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (4, "kick",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (5, "softban",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (6, "ban",))
            await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (7, "unban",))
            await db.commit()
        except Exception as e:
            return await msg.edit(content = f"FAILED TASK 3/4 because of \n{e}")
        await asyncio.sleep(2)
        await msg.edit(content=f"Creating blocklist database TASK 4/4")
        try:
            await db.execute("CREATE TABLE IF NOT EXISTS dmblocklist (name TEXT, userid INT)")
            await db.commit()
        except Exception as e:
            return await ctx.send(f"Failed task 4/4 because of \n{e}")
        await msg.edit(content = f"Closing database")
        try:
            await db.close()
        except ValueError:
            pass
        except Exception as e:
            return await msg.edit(content = f"Failed to close db because of \n{e}")
        await asyncio.sleep(2)
        await msg.edit(content =  "Done!")
    
    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, module = None):
        if module is not None:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
                return await ctx.send(f"Reloaded `{module}`")
            except MissingPermissions:
                return await ctx.send("You need to be a bot developer to access these commands.")
            except Exception as e:
                return await ctx.send(f"Failed to reload {module} due to an error: `{e}`")

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, module = None):
        try:
            self.bot.load_extension(module)
            return await ctx.send(f"Loaded `{module}`")
        except MissingPermissions:
            return await ctx.send("You need to be a bot developer to access these commands.")
        except Exception as e:
            return await ctx.send(f"Could not load {module} due to an error: `{e}`")
    
    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, module):
        try:
            self.bot.unload_extension(module)
            return await ctx.send(f"unloaded `{module}`")
        except MissingPermissions:
            return await ctx.send("You need to be a bot developer to access these commands.")
        except Exception as e:
            return await ctx.send(f"Could not unload {module} due to an error: `{e}`")





def setup(bot):
    bot.add_cog(dev(bot))