import feedparser
import aiohttp

async def fetch_updates(session):
    rss_url = 'https://www.mangaupdates.com/rss.php'
    manga_info = []

    try:
        async with session.get(rss_url) as resp:
            if resp.status != 200:
                return []
            content = await resp.text()
            
        # Parse synchronously (fast enough for text)
        data = feedparser.parse(content)
        
        for entry in data.entries:
            title_raw = entry['title']
            date = entry.get('summary', '').split('<br')[0]
            
            # Logic to extract Group/Author
            try:
                group = title_raw[title_raw.index('[')+1 : title_raw.index(']')]
                rest = title_raw.split(f'[{group}]')[1]
            except ValueError:
                group = "Unknown"
                rest = title_raw

            # Logic to extract Chapter
            chapter = "Unknown"
            if 'v.' in rest:
                parts = rest.rsplit('v.')
                if 'c.' in parts[1]:
                    chapter = parts[1].rsplit('c.')[1].strip()
            elif 'c.' in rest:
                chapter = rest.rsplit('c.')[1].strip()

            clean_title = rest.rsplit('c.')[0].strip() if 'c.' in rest else rest.strip()
            
            manga_info.append({
                'Title': clean_title,
                'Chapter': chapter,
                'Date': date,
                'Author': group,
                'Link': entry.get('link', ''),
                'Source': 'MangaUpdate'
            })
            
    except Exception:
        return []

    return manga_info