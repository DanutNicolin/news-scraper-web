from news_scraper.src.scraper import Digi24


scrapers = {  'A': 'Adevarul',
              'B': 'Digi24',
              'C': 'Mediafax',
              'D': 'Stirile ProTv',
              'E': 'Libertatea'
            }


def get_menu(menu: dict) -> list:
    parsed_menu = []
    for name in menu.values():
        parsed_menu.append(name)
    return parsed_menu
    

def make_scraper(website: str):
    if website == 'Digi24':
        scraper = Digi24()
        return scraper
    # if website == 'Adevarul':
    #     scraper = Adevarul()
    #     return scraper



options = {
    'A':'Print todays news',
    'B':'Search by key word',
    'C':'Add all titles to database',
    'D':'Plot words count'
} 