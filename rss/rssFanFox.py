import feedparser
from datetime import datetime

async def fetch_updates(session):
    rss_url = 'https://feeds2.feedburner.com/mangafox/latest_manga_chapters'
    manga_info = []

    try:
        async with session.get(rss_url) as resp:
            if resp.status != 200: 
                return []
            content = await resp.text()

        data = feedparser.parse(content)

        for entry in data.entries:
            title = entry['title']
            url = entry.get('feedburner_origlink', entry.get('link'))
            
            try:
                dt = datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S %Z')
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = datetime.today().strftime('%Y-%m-%d')

            # Extract Title and Chapter
            chapter = "0"
            clean_title = title
            
            if 'Vol.' in title:
                parts = title.rsplit('Vol.')
                clean_title = parts[0]
                if 'Ch.' in parts[1]:
                    chapter = parts[1].rsplit('Ch.')[1].strip()
            elif 'Ch.' in title:
                parts = title.rsplit('Ch.')
                clean_title = parts[0]
                chapter = parts[1].strip()

            clean_title = clean_title.replace('&apos;', "'").strip()

            manga_info.append({
                'Title': clean_title,
                'Chapter': chapter,
                'Date': date_str,
                'Author': 'FanFox',
                'Link': url
            })
            
    except Exception:
        pass
    
    return manga_info