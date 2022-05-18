import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions


class channelmoderation(commands.Cog):
    def __init__(self, bot):
        """Channel creation and tools."""
        self.bot = bot

    @commands.command(name="cchannel")
    async def cchannel(self, ctx, *, channelname=None):
        """Create a blanko channel."""
        if channelname is not None:
            channel =  await ctx.guild.create_text_channel(name=channelname)
            await ctx.send(f"Created channel {channel.name} ({channel.mention}")
        else:
            return await ctx.send("✖ You forgt to provide an channel name!")
    
    @commands.command(name="delchannel")
    async def delchannel(self, ctx, channel: discord.TextChannel = None):
        """Delete a channel from the server."""
        if channel is not None:
            try:
                await channel.delete()
                await ctx.send(f"Deleted {channel.name}!")
            except MissingPermissions:
                return await ctx.send("You do not have the right permissions to do so.")
        else:
            return await ctx.send("You did not mention a channel to delete.")










def setup(bot):
    bot.add_cog(channelmoderation(bot))