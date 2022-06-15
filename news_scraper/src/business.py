
from collections import defaultdict
from typing import Optional
from news_scraper.src.scraper import Digi24
from news_scraper.src.database import DataBaseManager
from operator import itemgetter
import re
import base64
from io import BytesIO
from matplotlib.figure import Figure



digi24 = Digi24()
db = DataBaseManager('database.db')



def get_all_titles(scraper):
    extracted_titles = []
    all_titles = scraper.scrape_titles()
    for title in all_titles:
        extracted_titles.append(title.strip())
    return extracted_titles


def get_titles_from_db(table_name: str, date: Optional[str]=None):
    db_data = db.retrieve_data(table_name, date)

    titles = []
    for data in db_data:
        titles.append(data[2].strip())
    return titles


def create_table(table_name: str):
    db.create_table(table_name)

def check_if_title_in_db(scraper_titles: list, db_titles: list):
    unsaved_titles = []

    for s_title in scraper_titles:
        if s_title in db_titles:
            continue
        else:
            unsaved_titles.append(s_title)
    return unsaved_titles

        
def add_title_in_db(scraper, title: str):
    db.add_data(str(scraper), title)


def parse_titles(titles: list):
    CONJUNCTIONS = ['și', 'și', 'nici', 'de', 'sau', 'ori', 'dacă', 'fiindcă', 'iar', 'dar', 'însă', 'ci', 'deci', 'că', 'să', 'ca', 'căci', 'deși', 'încât', 'deoarece',
     'ba', 'fie', 'cum', 'cu', 'cât', 'precum', 'așadar', 'prin', 'urmare', 'în', 'la', 'au', 'o', 'a', 'un', 'din', 'pentru', 'ce', 'cum', 'pe', 'sub', 'care', 'fost', 's',
     'înainte', 'după','ar', 'la', 'din', 'te', 'mai', 'vai', 'se', 'al', 'fi', 'nu', 'da', 'va', 'vă', 'îl', 'este', 'si', 'e', 'sunt', 'despre', 
     'i', 'asupra', 'putea', 'vor', 'într-o', 'într', 'lui']

    counts = defaultdict(int)
 
    for title in titles:
        for word in re.findall('\w+', title.lower()):
            if word in CONJUNCTIONS:
                continue
            else:
                counts[word] += 1
    return dict(counts)


def get_top_words(words: dict, n: int):
    n = int(n)
    top_n_words = dict(sorted(words.items(), key = itemgetter(1), reverse = True)[:n])
    return top_n_words


def plot(data: dict, date:str):
    words = list(data.keys())
    count = list(data.values())

    # Generate the figure **without using pyplot**.
    fig = Figure()
    if (len(words) < 8) and (len(count) < 5.5):
        fig.set_size_inches(8,5.5)
    else:
        fig.set_size_inches(len(words),len(count))

    ax = fig.subplots()
    ax.plot(words, count)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    