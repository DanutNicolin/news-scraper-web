
from news_scraper.src import scraper
from news_scraper.src.scraper import Digi24
from news_scraper.src.commands import Command
from news_scraper.src.business import get_option_choice
from typing import Optional, Callable, Union
from news_scraper.src.commands import PrintAllTitles, PrintKeywords, Exit, WriteToDataBase, PlotData

from news_scraper.src.business import get_option_choice


 



scrapers = {  'A': 'Adevarul',
              'B': 'Digi24',
              'C': 'Mediafax',
              'D': 'Stirile ProTv',
              'E': 'Libertatea'
            }

class Option:
    def __init__(
        self,
        name: str,
        command: Command,
        prep_call: Optional[Callable]=None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def _handle_message(self, message: Union[str, list]):
        if isinstance(message, list):
            for entry in message:
                print(entry)
        else:
            print(message)

    def choose(self):
        data = None
        if self.prep_call:
            data = self.prep_call()
        if data:
            try:
                message = self.command.execute(data)
            except:
                message = self.command.execute(data[0], data[1])
        else:
            message = self.command.execute()
        print()

    def __str__(self):
        return self.name




def print_websites():
    for website in scrapers.items():
        print(website[0], website[1])
    print()



def print_menu(menu: dict):
    print('')
    for (option, name) in zip(menu.keys(), menu.values()):
        print(f'{option} {name}')
    print('')


def get_menu(menu: dict) -> list:
    parsed_menu = []
    for name in menu.values():

        parsed_menu.append(name)
    return parsed_menu


def get_scraper():
    print_websites()
    chosen_option = get_option_choice(scrapers)
    return chosen_option

def make_scraper(website: str):
    if website == 'Digi24':
        scraper = Digi24()
        return scraper
    # if website == 'Adevarul':
    #     scraper = Adevarul()
    #     return scraper



options = {
    'A': Option('Print todays news', PrintAllTitles(), prep_call=get_scraper),
    'B': Option('Search by key word', PrintKeywords(), prep_call=get_scraper),
    'C': Option('Add all titles to database', WriteToDataBase(), prep_call=get_scraper),
    'D': Option('Plot words count', PlotData(), prep_call=get_scraper),
} 