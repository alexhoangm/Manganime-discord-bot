import os
import discord
import logging
import asyncio
import aiohttp
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from dotenv import load_dotenv

# Import modules
import db.dbsqlite as db
import mdexapi
import rss.rssMangaUpdate as rssMU
import rss.rssFanFox as rssFF
import rss.rssScanlatorsParser as rssSP

# Logging Setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', filename='bot.log')
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

# Global Session
bot.session = None

@bot.event
async def on_ready():
    # Initialize DB and Session
    await db.init_db()
    bot.session = aiohttp.ClientSession()
    
    # Start Background Tasks
    if not check_updates_task.is_running():
        check_updates_task.start()
        
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is Ready.')

@bot.event
async def on_close():
    if bot.session:
        await bot.session.close()

# Background Task
@tasks.loop(minutes=30)
async def check_updates_task():
    logger.info("Starting background update check...")
    
    # 1. Check MangaUpdates
    try:
        new_data = await rssMU.fetch_updates(bot.session)
        # (Simplified logic: In real app, compare with DB to find *new* chapters)
        # For now, we just populate the cache
        msg_list = [(x['Title'], x['Chapter'], x['Author'], x['Date']) for x in new_data]
        await db.populate_mangaupdate_table(msg_list)
    except Exception as e:
        logger.error(f"Error in MangaUpdates loop: {e}")

    # 2. Check FanFox
    try:
        new_data = await rssFF.fetch_updates(bot.session)
        msg_list = [(x['Title'], x['Chapter'], x['Author'], x['Date'], x['Link']) for x in new_data]
        await db.populate_fanfox_table(msg_list)
    except Exception as e:
        logger.error(f"Error in FanFox loop: {e}")

    # 3. Check Scanlators
    try:
        new_data = await rssSP.fetch_updates(bot.session)
        msg_list = [(x['Title'], x['Chapter'], x['Author'], x['Date'], x['Link']) for x in new_data]
        await db.populate_scanlator_table(msg_list)
    except Exception as e:
        logger.error(f"Error in Scanlators loop: {e}")
        
    logger.info("Update check complete.")

@check_updates_task.before_loop
async def before_check_updates():
    await bot.wait_until_ready()

# Slash Commands
@slash.slash(name='ping', description='Check latency')
async def ping(ctx: SlashContext):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@slash.slash(name='find', description='Find and follow a manga')
async def find(ctx: SlashContext, title: str):
    await ctx.defer() # Vital for async API calls
    
    data = await mdexapi.title_result(title, bot.session)
    
    if not data:
        await ctx.send("Manga not found.", hidden=True)
        return

    m_title = mdexapi.get_manga_title(data)
    m_desc = mdexapi.get_manga_description(data)
    m_link = mdexapi.get_manga_link(data)
    m_id = mdexapi.get_manga_id(data)
    cover_file = await mdexapi.get_cover_id(m_id, bot.session)
    cover_url = f"https://uploads.mangadex.org/covers/{m_id}/{cover_file}" if cover_file else ""

    embed = discord.Embed(title=m_title, url=m_link, description=m_desc[:500] + "...")
    if cover_url:
        embed.set_thumbnail(url=cover_url)
    
    buttons = [
        create_button(style=ButtonStyle.green, label="Follow", custom_id="yes"),
        create_button(style=ButtonStyle.red, label="Cancel", custom_id="no")
    ]
    action_row = create_actionrow(*buttons)

    msg = await ctx.send(embed=embed, components=[action_row])

    def check(res):
        return res.origin_message_id == msg.id and res.author_id == ctx.author.id

    try:
        res = await wait_for_component(bot, components=action_row, check=check, timeout=15)
        if res.component['label'] == "Follow":
            # Add to DB
            user_exists = await db.select_userguild(ctx.author.id)
            if not user_exists:
                await db.populate_mangauser_table([(ctx.guild.id, str(ctx.author), ctx.author.id, m_title)])
            else:
                # Add specific follow logic here (simplified)
                pass
            
            await res.edit_origin(content=f"✅ Following **{m_title}**", components=[])
        else:
            await res.edit_origin(content="❌ Cancelled", components=[])
    except asyncio.TimeoutError:
        await msg.edit(components=[])

bot.run(TOKEN)