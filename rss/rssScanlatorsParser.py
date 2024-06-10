import feedparser
import asyncio
from datetime import datetime


#Remove Tritinia Scans rss due to rss feed not updated
rssScanlator = {
'Arang Scans': 'https://arangscans.com/rss',
'Flame Scans'         : 'https://flamescans.org/feed/',
'Hatigarm Scans'      : 'https://hatigarmscanz.net/feed',
'Hunlight Scans'      : 'https://hunlight-scans.info/feed',
'Kirei Cake'          : 'https://kireicake.com/feed/',
'LHTranslation'       : 'https://lhtranslation.net/manga-rss.rss',
'Lynx Scans'          : 'https://lynxscans.com/feed',
'Mangasushi'          : 'https://mangasushi.net/feed/manga-chapters',
'MethodScan'          : 'https://methodscans.com/feed',
'NANI? Scans'         : 'https://naniscans.com/rss',
'SensesScans'         : 'https://sensescans.com/index.php?action=.xml;type=rss;board=45.0;sa=news',
'WhimSubs'            : 'https://whimsubs.xyz/r/feeds/rss.xml',
'Zero Scans (Discord)': 'https://zeroscans.com/feed'}

def parse_single_feed(content, author):
    results = []
    data = feedparser.parse(content)
    
    for entry in data.entries:
        try:
            title = entry['title']
            link = entry['link']
            # Date Parsing
            raw_date = entry.get('published', entry.get('updated', ''))
            try:
                dt = datetime.strptime(raw_date, '%a, %d %b %Y %H:%M:%S %z')
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = datetime.today().strftime('%Y-%m-%d')

            # Basic Chapter Extraction Strategy
            chapter = "0"
            clean_title = title
            
            if 'Chapter' in title:
                parts = title.split('Chapter')
                clean_title = parts[0].strip()
                chapter = parts[1].split()[0].strip()
            elif 'Ch.' in title:
                parts = title.split('Ch.')
                clean_title = parts[0].strip()
                chapter = parts[1].split()[0].strip()

            results.append({
                'Title': clean_title.strip('- '), 
                'Chapter': chapter, 
                'Date': date_str, 
                'Author': author, 
                'Link': link
            })
        except:
            continue
    return results

async def fetch_single(session, author, url):
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                content = await resp.text()
                return parse_single_feed(content, author)
    except:
        pass
    return []

async def fetch_updates(session):
    tasks = [fetch_single(session, author, url) for author, url in SCANLATORS.items()]
    results = await asyncio.gather(*tasks)
    
    # Flatten list
    flat_results = [item for sublist in results for item in sublist]
    return flat_results