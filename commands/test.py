import discord
from discord.ext import commands
import subprocess
import re
from bot import banned_users, create_ban_embed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger() 

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="neofetch", description="Returns the output of neofetch", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def neofetch(self, ctx):
        logger.info(f"User {ctx.author.name} (ID: {ctx.author.id}) ran the command: '{ctx.command.qualified_name}'")
        if ctx.author.id in banned_users:
            embed = create_ban_embed(ctx, ctx.author.id)
            await ctx.respond(embed=embed)
            return

        result = subprocess.run(['neofetch', '--off'], capture_output=True, text=True)

        clean_output = self.strip_ansi(result.stdout)

        if result.returncode != 0:
            error_output = result.stderr.strip()
            print(f"Error: {error_output}")
            await ctx.respond(f"Error running neofetch: {error_output}")
            return

        await ctx.respond(f"```\n{clean_output}```")

    def strip_ansi(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]?|\x1B\[[0-?9;]*[h?]|[\x1B\x9B][0-??]*[0-??9]*[mG]')
        return ansi_escape.sub('', text)

def setup(bot):
    bot.add_cog(Test(bot))
