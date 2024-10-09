import discord
from discord import option
from discord.ext import commands
import requests
import json
from bot import banned_users, create_ban_embed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class DomainCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="domain", description="Check if a domain is avaliable", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @option("domain", description="Domain to register", required=True)
    async def domain(self, ctx, domain: str):
        logger.info(f"User {ctx.author.name} (ID: {ctx.author.id}) ran the command: '{ctx.command.qualified_name}'")
        if ctx.author.id in banned_users:
            embed = create_ban_embed(ctx, ctx.author.id)
            await ctx.respond(embed=embed)
            return

        url = "https://api.frii.site/domain-is-avaliable"
        payload = {
            "domain": domain,
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                await ctx.respond(f"Domain {domain} is avaliable!")
            else:
                logger.error(f"Failed to register domain. Status code: {response.status_code}")
                await ctx.respond(f"Failed to register domain {domain}. Status code: {response.status_code}")
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(DomainCommand(bot))
