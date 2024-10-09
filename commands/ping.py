import discord
from discord import option
from discord.ext import commands
import requests
import json
from bot import banned_users, create_ban_embed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Pong!", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def ping(self, ctx):
        logger.info(f"User {ctx.author.name} (ID: {ctx.author.id}) ran the command: '{ctx.command.qualified_name}'")
        if ctx.author.id in banned_users:
            embed = create_ban_embed(ctx, ctx.author.id) 
            await ctx.respond(embed=embed)
            return

        await ctx.respond("Pong!")



def setup(bot):
    bot.add_cog(Ping(bot))
