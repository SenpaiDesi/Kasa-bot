import discord
from discord.ext import commands, tasks
import re
import asyncio
import aiosqlite
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}



class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        global args
        global time
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time, args
    

class fun(commands.Cog):
    """Fun commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(seconds=1, count=20)
    async def automsg_loop(self, interval, msg):
        channel = self.bot.get_channel(channel_raw)
        await channel.send(msg)
        await asyncio.sleep(interval)
    
    @commands.command(name="automsg")
    async def automsg (self, ctx, msgInterval: TimeConverter, *, message):
        """Set an auto message loop. Format automsg interval message here. EXAMPLE: kasa-automsg 3s Hello there."""
        global channel_raw 
        channel_raw = ctx.channel.id
        try:
            self.automsg_loop.start(time, message)
        except RuntimeError:
            return await ctx.send("Another message loop is running. Use kasa-stop to stop that first.")
    @commands.command(name="stoploop", aliases=["slp", "stop"])
    async def stop(self, ctx):
        """Stops the auto message loop."""
        self.automsg_loop.stop()
        await ctx.send("Stopped auto message loop")
    
    @commands.command(name="dm")
    async def dm(self, ctx, member : discord.Member=None, *, message):
        """Dm an user from your server."""
        db = await aiosqlite.connect("./database.db")
        
    






def setup(bot):
    bot.add_cog(fun(bot))