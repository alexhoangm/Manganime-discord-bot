import aiohttp
import logging

logger = logging.getLogger(__name__)

async def title_result(title, session):
    clean_title = title.replace(' ', '+')
    try:
        async with session.get(f'https://api.mangadex.org/manga?title={clean_title}') as resp:
            if resp.status == 200:
                data = await resp.json()
                return data if data.get('data') else None
    except Exception as e:
        logger.error(f"Error fetching title: {e}")
    return None

def get_manga_id(data):
    try:
        return data['data'][0]['id']
    except (IndexError, KeyError, TypeError):
        return None

def get_manga_title(data):
    try:
        return data['data'][0]['attributes']['title']['en']
    except (IndexError, KeyError, TypeError):
        return None

def get_manga_description(data):
    try:
        desc = data['data'][0]['attributes']['description']['en']
        return desc.split('\n')[0].strip() if desc else 'No description available.'
    except (IndexError, KeyError, TypeError):
        return 'Not found'

def get_manga_link(data):
    m_id = get_manga_id(data)
    title = get_manga_title(data)
    if m_id and title:
        slug = title.lower().replace(',', '').replace(' ', '-')
        return f'https://mangadex.org/title/{m_id}/{slug}'
    return 'Not found'

def get_manga_list(data):
    titles = []
    try:
        for entry in data['data'][:10]:
            titles.append(entry['attributes']['title'].get('en', 'Unknown Title'))
    except (IndexError, KeyError, TypeError):
        pass
    # Remove duplicates preserving order
    return list(dict.fromkeys(titles))

async def get_cover_id(manga_id, session):
    try:
        async with session.get(f'https://api.mangadex.org/cover?manga[]={manga_id}') as resp:
            data = await resp.json()
            return data['data'][0]['attributes']['fileName']
    except (IndexError, KeyError, TypeError, Exception):
        return None

async def get_chapter_link(manga_id, chapter_num, session):
    try:
        async with session.get(f'https://api.mangadex.org/chapter?manga={manga_id}&chapter={chapter_num}') as resp:
            data = await resp.json()
            for entry in data.get('data', []):
                if entry['attributes']['translatedLanguage'] == 'en':
                    return f"https://mangadex.org/chapter/{entry['id']}/1"
    except Exception:
        pass
    return None