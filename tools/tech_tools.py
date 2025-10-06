# Tech & AI News Tools
import os
from newsapi import NewsApiClient
import requests
import feedparser
from bs4 import BeautifulSoup
import urllib.parse
import time

def safe_get_top_headlines(newsapi, params, retries=2, delay=2):
    for attempt in range(retries):
        try:
            result = newsapi.get_top_headlines(**params)
            if result is not None:
                return result
            else:
                return {'articles': []}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                # Optionally log the error
                # print(f"NewsAPI request failed after {retries} attempts: {e}")
                return {'articles': []}
    return {'articles': []}

def get_latest_tech_news(region: str = ""):
    """
    Fetch the latest technology news headlines using NewsAPI and GNews. Optionally filter by region (country name or code).
    Returns a list of news dicts with 'title', 'description', and 'url'.
    """
    api_key = os.getenv('NEWSAPI_KEY')
    gnews_api_key = os.getenv('GNEWS_API_KEY')
    country_map = {
        'india': 'in', 'bharat': 'in', 'us': 'us', 'usa': 'us', 'united states': 'us',
        'uk': 'gb', 'united kingdom': 'gb', 'england': 'gb', 'canada': 'ca', 'australia': 'au',
        'germany': 'de', 'france': 'fr', 'china': 'cn', 'japan': 'jp', 'russia': 'ru',
        'brazil': 'br', 'south africa': 'za', 'italy': 'it', 'spain': 'es', 'pakistan': 'pk',
        'bangladesh': 'bd', 'indonesia': 'id', 'mexico': 'mx', 'turkey': 'tr', 'uae': 'ae',
        'singapore': 'sg', 'new zealand': 'nz', 'saudi arabia': 'sa', 'argentina': 'ar',
        'south korea': 'kr', 'korea': 'kr', 'egypt': 'eg', 'nigeria': 'ng', 'kenya': 'ke',
        'sweden': 'se', 'norway': 'no', 'denmark': 'dk', 'finland': 'fi', 'switzerland': 'ch',
        'netherlands': 'nl', 'belgium': 'be', 'poland': 'pl', 'portugal': 'pt', 'greece': 'gr',
        'israel': 'il', 'malaysia': 'my', 'thailand': 'th', 'philippines': 'ph', 'vietnam': 'vn',
        'colombia': 'co', 'chile': 'cl', 'peru': 'pe', 'venezuela': 've', 'iran': 'ir', 'iraq': 'iq',
        'afghanistan': 'af', 'sri lanka': 'lk', 'nepal': 'np', 'myanmar': 'mm', 'taiwan': 'tw',
        'hong kong': 'hk', 'ireland': 'ie', 'austria': 'at', 'czech': 'cz', 'czech republic': 'cz',
        'romania': 'ro', 'hungary': 'hu', 'bulgaria': 'bg', 'croatia': 'hr', 'slovakia': 'sk',
        'slovenia': 'si', 'estonia': 'ee', 'latvia': 'lv', 'lithuania': 'lt', 'luxembourg': 'lu',
        'iceland': 'is', 'malta': 'mt', 'cyprus': 'cy', 'georgia': 'ge', 'kazakhstan': 'kz',
        'ukraine': 'ua', 'belarus': 'by', 'serbia': 'rs', 'montenegro': 'me', 'albania': 'al',
        'bosnia': 'ba', 'macedonia': 'mk', 'moldova': 'md', 'armenia': 'am', 'azerbaijan': 'az',
        'uzbekistan': 'uz', 'turkmenistan': 'tm', 'kyrgyzstan': 'kg', 'tajikistan': 'tj',
        'mongolia': 'mn', 'north korea': 'kp', 'palestine': 'ps', 'jordan': 'jo', 'lebanon': 'lb',
        'syria': 'sy', 'yemen': 'ye', 'oman': 'om', 'qatar': 'qa', 'bahrain': 'bh', 'kuwait': 'kw',
        'morocco': 'ma', 'algeria': 'dz', 'tunisia': 'tn', 'libya': 'ly', 'sudan': 'sd',
        'ethiopia': 'et', 'tanzania': 'tz', 'uganda': 'ug', 'zambia': 'zm', 'zimbabwe': 'zw',
        'botswana': 'bw', 'namibia': 'na', 'angola': 'ao', 'mozambique': 'mz', 'madagascar': 'mg',
        'cameroon': 'cm', 'ghana': 'gh', 'senegal': 'sn', 'mali': 'ml', 'niger': 'ne', 'chad': 'td',
        'burkina faso': 'bf', 'benin': 'bj', 'togo': 'tg', 'sierra leone': 'sl', 'liberia': 'lr',
        'cote d ivoire': 'ci', 'ivory coast': 'ci', 'gabon': 'ga', 'congo': 'cg', 'congo drc': 'cd',
        'central african republic': 'cf', 'guinea': 'gn', 'guinea-bissau': 'gw', 'gambia': 'gm',
        'mauritania': 'mr', 'somalia': 'so', 'djibouti': 'dj', 'eritrea': 'er', 'malawi': 'mw',
        'rwanda': 'rw', 'burundi': 'bi', 'lesotho': 'ls', 'swaziland': 'sz', 'eswatini': 'sz',
        'seychelles': 'sc', 'mauritius': 'mu', 'cape verde': 'cv', 'comoros': 'km', 'sao tome': 'st',
        'equatorial guinea': 'gq', 'guadeloupe': 'gp', 'martinique': 'mq', 'reunion': 're',
        'mayotte': 'yt', 'new caledonia': 'nc', 'fiji': 'fj', 'samoa': 'ws', 'tonga': 'to',
        'vanuatu': 'vu', 'solomon islands': 'sb', 'papua new guinea': 'pg', 'palau': 'pw',
        'marshall islands': 'mh', 'micronesia': 'fm', 'kiribati': 'ki', 'tuvalu': 'tv',
        'northern mariana islands': 'mp', 'guam': 'gu', 'puerto rico': 'pr', 'us virgin islands': 'vi',
        'bermuda': 'bm', 'greenland': 'gl', 'aruba': 'aw', 'curacao': 'cw', 'cayman islands': 'ky',
        'gibraltar': 'gi', 'jersey': 'je', 'guernsey': 'gg', 'isle of man': 'im', 'monaco': 'mc',
        'san marino': 'sm', 'vatican': 'va', 'liechtenstein': 'li', 'andorra': 'ad', 'faroe islands': 'fo',
        'alderney': 'gg', 'sark': 'gg', 'herm': 'gg', 'bailiwick of guernsey': 'gg', 'bailiwick of jersey': 'je',
        'saint helena': 'sh', 'saint pierre': 'pm', 'saint barthelemy': 'bl', 'saint martin': 'mf',
        'saint vincent': 'vc', 'saint lucia': 'lc', 'saint kitts': 'kn', 'saint croix': 'vi',
        'saint thomas': 'vi', 'saint john': 'vi', 'anguilla': 'ai', 'antigua': 'ag', 'barbados': 'bb',
        'bahamas': 'bs', 'grenada': 'gd', 'dominica': 'dm', 'st vincent': 'vc', 'st lucia': 'lc',
        'st kitts': 'kn', 'st croix': 'vi', 'st thomas': 'vi', 'st john': 'vi', 'caribbean': '',
    }
    region_key = region.strip().lower()
    country_code = country_map.get(region_key, '')
    # --- NewsAPI Top Headlines ---
    newsapi_results = []
    if api_key:
        newsapi = NewsApiClient(api_key=api_key)
        params = {'category': 'technology', 'language': 'en', 'page_size': 10}
        if country_code:
            params['country'] = country_code
        top_headlines = safe_get_top_headlines(newsapi, params)
        articles = top_headlines.get('articles', [])
        if not articles and country_code:
            params.pop('country', None)
            top_headlines = safe_get_top_headlines(newsapi, params)
            articles = top_headlines.get('articles', [])
        newsapi_results = [
            {
                'title': a['title'],
                'description': a['description'],
                'url': a['url']
            } for a in articles if a.get('title')
        ]
    # --- GNews Top Headlines ---
    gnews_results = []
    if gnews_api_key and not newsapi_results:
        gnews_url = f'https://gnews.io/api/v4/top-headlines?token={gnews_api_key}&lang=en&max=10&topic=technology'
        if country_code:
            gnews_url += f'&country={country_code}'
        resp = requests.get(gnews_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            gnews_results = [
                {
                    'title': a['title'],
                    'description': a.get('description') or a.get('content', ''),
                    'url': a['url']
                } for a in data.get('articles', []) if a.get('title')
            ]
    # --- Google News RSS ---
    google_news_results = []
    if not newsapi_results and not gnews_results:
        query = region_key + ' technology' if region_key else 'technology'
        encoded_query = urllib.parse.quote(query)
        rss_url = f'https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en' if region_key else 'https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en'
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:10]:
            google_news_results.append({
                'title': entry.title,
                'description': entry.summary if hasattr(entry, 'summary') else '',
                'url': entry.link
            })
    # --- Combine and deduplicate ---
    all_results = newsapi_results
    all_titles = {a['title'] for a in all_results}
    for item in gnews_results + google_news_results:
        if item['title'] not in all_titles:
            all_results.append(item)
            all_titles.add(item['title'])
    # --- Final fallback: NewsAPI get_everything and GNews search ---
    if not all_results:
        # NewsAPI get_everything (no country param)
        if api_key:
            everything_params = {'q': 'technology', 'language': 'en', 'page_size': 10}
            try:
                everything = newsapi.get_everything(**everything_params)
            except Exception:
                everything = {'articles': []}
            articles = everything.get('articles', [])
            all_results = [
                {
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url']
                } for a in articles if a.get('title')
            ]
        # GNews search
        if gnews_api_key and not all_results:
            gnews_url = f'https://gnews.io/api/v4/search?token={gnews_api_key}&lang=en&max=10&q=technology'
            if country_code:
                gnews_url += f'&country={country_code}'
            resp = requests.get(gnews_url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                all_results = [
                    {
                        'title': a['title'],
                        'description': a.get('description') or a.get('content', ''),
                        'url': a['url']
                    } for a in data.get('articles', []) if a.get('title')
                ]
        # Google News RSS fallback (final fallback)
        if not all_results:
            query = region_key + ' technology' if region_key else 'technology'
            encoded_query = urllib.parse.quote(query)
            rss_url = f'https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en' if region_key else 'https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en'
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:10]:
                all_results.append({
                    'title': entry.title,
                    'description': entry.summary if hasattr(entry, 'summary') else '',
                    'url': entry.link
                })
    if not all_results:
        return [{
            'title': 'No major news found',
            'description': 'No trending tech news found for your region or globally at this time.',
            'url': ''
        }]
    return all_results

# def get_ai_model_updates():
#     """
#     Fetch recent AI model updates from HuggingFace's model page (placeholder logic).
#     Returns a list of dicts with 'title', 'description', and 'url'.
#     """
#     url = 'https://huggingface.co/models?sort=trending'
#     try:
#         resp = requests.get(url, timeout=10)
#         soup = BeautifulSoup(resp.text, 'html.parser')
#         models = []
#         for card in soup.select('div[data-testid="model-card"]')[:10]:
#             link_tag = card.select_one('a[data-testid="model-card-link"]')
#             title = link_tag.text.strip() if link_tag and link_tag.text else 'Unknown Model'
#             link = 'https://huggingface.co' + link_tag['href'] if link_tag and link_tag.has_attr('href') else url
#             desc = card.select_one('div[data-testid="model-card-description"]')
#             models.append({
#                 'title': title,
#                 'description': desc.text.strip() if desc and desc.text else '',
#                 'url': link
#             })
#         return models
#     except Exception as e:
#         return [{
#             'title': 'Error fetching AI model updates',
#             'description': str(e),
#             'url': url
#         }] 