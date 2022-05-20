import discord
from discord.channel import CategoryChannel
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import asyncio
from moderation import perms

class channelmoderation(commands.Cog):
    """Channel creation and tools."""
    def __init__(self, bot):
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
                await ctx.send(f"Deleted `#{channel.name}!`")
            except MissingPermissions:
                return await ctx.send("You do not have the right permissions to do so.")
        else:
            return await ctx.send("You did not mention a channel to delete.")
            
    @commands.command(name="serversetup", aliases = ["ss"])
    @commands.has_permissions(manage_messages=True)
    async def server_setup(self, ctx):
        await ctx.send("Creating server from standard template...")
        await asyncio.sleep(2)

        
        try:
            staff_role = await ctx.guild.create_role(name="Staff", color = discord.Color.gold(), permissions =perms.staff_permissions, position=1 )
            member_role = await ctx.guild.create_role(name="member", color = discord.Color.blue(), permissions = perms.member_roles, position=5)
            welcome_cat =  await ctx.guild.create_category_channel(name="Welcome", position=0)
            welcome_channel1 = await ctx.guild.create_text_channel(name="Welcome-goodbye", category = welcome_cat)
            welcome_channel2 = await ctx.guild.create_text_channel(name="Rules", category = welcome_cat)
            welcome_channel3 = await ctx.guild.create_text_channel(name="Roles", category = welcome_cat)
            General_cat = await ctx.guild.create_category_channel(name="General", position=1)
            general_channel1 = await ctx.guild.create_text_channel(name="General-Chat", category = General_cat)
            general_channel2 = await ctx.guild.create_text_channel(name="Bot-Commands", category = General_cat)
            general_channel3 = await ctx.guild.create_text_channel(name="Memes", category=General_cat)
            general_voice1 = await ctx.guild.create_voice_channel(name="Voice-One", category = General_cat)
            general_voice2 = await ctx.guild.create_voice_channel(name="Voice-Two", category = General_cat)
        except Exception as e:
            return await ctx.send(e)









def setup(bot):
    bot.add_cog(channelmoderation(bot))