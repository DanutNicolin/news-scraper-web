
from collections import defaultdict
from typing import Optional
from news_scraper.src.scraper import Digi24
from news_scraper.src.database import DataBaseManager
from matplotlib import pyplot as plt
from operator import itemgetter
from news_scraper.src.utils import clear_screen
import re
import base64
from io import BytesIO
from matplotlib.figure import Figure



digi24 = Digi24()
db = DataBaseManager('database.db')
curent_date = str(digi24.curent_date())


def option_choice_is_valid(choice: str, options: dict):
    if choice.upper() in options.keys():
        return True
    else:
        return False


def get_option_choice(options: dict):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice!")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_date():
    options = {'A': '- aaaCurent date', 'B': '- Input date', 'C': '- All the dates'}
    for option in options.items():
        print(option[0], option[1])
    print('')

    choice = get_option_choice(options)
    clear_screen()

    if choice == '- All the dates':
        return None
    if choice == '- Curent date':
        return curent_date
    if choice == '- Input date':
        date = str(input('Input date (dd.mm.yyyy): '))
        return date


def get_date_flask():
    options = {'A': '- Curent date', 'B': '- Input date', 'C': '- All the dates'}
    for option in options.items():
        print(option[0], option[1])
    print('')

    choice = get_option_choice(options)
    clear_screen()

    if choice == '- All the dates':
        return None
    if choice == '- Curent date':
        return curent_date
    if choice == '- Input date':
        date = str(input('Input date (dd.mm.yyyy): '))
        return date




def get_all_titles(scraper):
    extracted_titles = []
    all_titles = scraper.scrape_titles()
    for title in all_titles:
        extracted_titles.append(title.strip())
    return extracted_titles


def get_date_from_db(table_name: str):
    db_data = db.retrieve_data(table_name)

    dates = []
    for date in db_data:
        dates.append(date[1])
    return dates



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


def plot_data(data: dict, date: str, db_date: list):
    db_date = [db_date[0], db_date[-1]]

    if date == None:
        date = f' between {db_date[0]} - {db_date[1]}'

    words = list(data.keys())
    count = list(data.values())

    plt.bar(words, count)

    plt.xlabel('Words')
    plt.ylabel('Number of ocurencyes')
    plt.title(f'Word frequency {date}')

    return plt.show()

def plot_flask(data: dict, date:str, db_date: list):

    if date == None:
        date = f' between {db_date[0]} - {db_date[1]}'

    words = list(data.keys())
    count = list(data.values())

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
    # return f"<img src='data:image/png;base64,{data}'/>"
    