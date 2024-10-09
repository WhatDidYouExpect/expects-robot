import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import json

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

banned_users = {}

def load_banned_users():
    global banned_users
    with open('bans.json') as f:
        bans_data = json.load(f)
    banned_users = {int(user_id): reason for user_id, reason in bans_data.items()}

load_banned_users()

def create_ban_embed(ctx, user_id):
    reason = banned_users.get(user_id, "No reason provided.")
    logger.warning(f"User {user_id} is already banned and tried running a command.")
    embed = discord.Embed(
        title="You are Banned :3", 
        description=f"Reason: {reason}", 
        color=discord.Color.red()
    )
    embed.set_footer(text=f"{ctx.author.name} is a disappointment", icon_url=ctx.author.avatar.url)
    return embed

intents = discord.Intents.default()
intents.members = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

@bot.event
async def on_command(ctx):
    """Logs the user and the command they ran."""
    logger.info(f"User {ctx.author.name} (ID: {ctx.author.id}) ran the command: '{ctx.command.qualified_name}'")

@bot.event
async def on_command_error(ctx, error):
    """Handles command errors."""
    if isinstance(error, commands.CheckFailure):
        return 

    logger.error(f"Error in command '{ctx.command.qualified_name}': {error}")
    await ctx.send("An error occurred while processing your command.")

for filename in os.listdir('./commands'):
    if filename.endswith('.py') and filename != '__init__.py':
        bot.load_extension(f'commands.{filename[:-3]}')
        logger.info(f'Loaded commands.{filename[:-3]}')

bot.run(TOKEN)
