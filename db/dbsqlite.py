import aiosqlite
import logging

logger = logging.getLogger(__name__)
DB_NAME = 'botuser.db'

async def init_db():
    """Initializes the database tables if they do not exist."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS guildinfo(
            guildname TEXT NOT NULL, guildid INTEGER)''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS mangauser(
            guildid INTEGER, username TEXT NOT NULL, userid INTEGER, title TEXT NOT NULL)''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS mangaupdate(
            title TEXT NOT NULL, chapter INTEGER, author TEXT NOT NULL, date DATE)''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS scanlator(
            title TEXT NOT NULL, chapter INTEGER, author TEXT NOT NULL, date DATE, link TEXT NOT NULL)''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS fanfox(
            title TEXT NOT NULL, chapter INTEGER, author TEXT NOT NULL, date DATE, link TEXT NOT NULL)''')
        
        await db.commit()
        logger.info("Database initialized.")

# ================= SELECT QUERIES =================

async def select_guild(guildid) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT guildid FROM guildinfo WHERE guildid = ?', (guildid,)) as cursor:
            record = await cursor.fetchone()
            return record is not None

async def select_userguild(userid):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT userid FROM mangauser WHERE userid = ?', (userid,)) as cursor:
            record = await cursor.fetchone()
            return record

async def select_follow(title):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT userid FROM mangauser WHERE title = ?', (title,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def select_specfollow(userid):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT title FROM mangauser WHERE userid = ?', (userid,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def select_viewall(userid):
    return await select_specfollow(userid)

async def select_altlinkscan(title):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT link FROM scanlator WHERE title = ?', (title,)) as cursor:
            record = await cursor.fetchone()
            return record[0] if record else None

async def select_altlinkfox(title):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT link FROM fanfox WHERE title = ?', (title,)) as cursor:
            record = await cursor.fetchone()
            return record[0] if record else None

# ================= POPULATE QUERIES =================

async def populate_guild_table(recordlist):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany('INSERT INTO guildinfo(guildname, guildid) VALUES(?, ?)', recordlist)
        await db.commit()

async def populate_mangauser_table(recordlist):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany('INSERT INTO mangauser(guildid, username, userid, title) VALUES(?, ?, ?, ?)', recordlist)
        await db.commit()

async def populate_mangaupdate_table(recordlist):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany('INSERT INTO mangaupdate(title, chapter, author, date) VALUES(?, ?, ?, ?)', recordlist)
        await db.commit()

async def populate_scanlator_table(recordlist):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany('INSERT INTO scanlator(title, chapter, author, date, link) VALUES(?, ?, ?, ?, ?)', recordlist)
        await db.commit()

async def populate_fanfox_table(recordlist):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany('INSERT INTO fanfox(title, chapter, author, date, link) VALUES(?, ?, ?, ?, ?)', recordlist)
        await db.commit()

# ================= DELETE QUERIES =================

async def delete_guild(guildid):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM guildinfo WHERE guildid = ?', (guildid,))
        await db.execute('DELETE FROM mangauser WHERE guildid = ?', (guildid,))
        await db.commit()

async def delete_user(userid):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM mangauser WHERE userid = ?', (userid,))
        await db.commit()

async def delete_user_unfollow(title, userid):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM mangauser WHERE title = ? AND userid = ?', (title, userid))
        await db.commit()