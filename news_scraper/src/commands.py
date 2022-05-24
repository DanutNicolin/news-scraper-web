
from news_scraper.src.business import (
    get_all_titles,
    get_date_from_db,
    get_titles_from_db,
    create_table,
    check_if_title_in_db,
    add_title_in_db,
    get_top_words,
    parse_titles,
    digi24,
    plot_data,
    get_date
    )
from typing import Optional
from news_scraper.src.utils import clear_screen
import sys





class Command:
    def execute(self):
        raise NotImplementedError()





class GetAllTitles:
    def execute(self, scraper):
        extracted_titles = get_all_titles(scraper)
        return extracted_titles


class PrintAllTitles: 
    def execute(self, scraper):
        clear_screen()
        extracted_titles = GetAllTitles().execute(scraper)
        for title in extracted_titles:
            print(title)




        
class SearchKeyword:
    def execute(self, scraper, keyword: str):
        all_titles = GetAllTitles().execute(scraper)
        filtered_titles = []

        for title in all_titles:
            if keyword in title.lower():
                filtered_titles.append(title)
        return filtered_titles


class PrintKeywords:
    def execute(self, scraper):
        keyword = input('Input keyword: ')
        filtered_titles = SearchKeyword().execute(scraper, keyword)
        clear_screen()
        if len(filtered_titles)>0:
            for title in filtered_titles:
                print(title)
        else:
            print(f'No title found with {keyword} keyword')





class Exit:
    def execute(self):
        sys.exit()


class GetDate:
    def execute(self):
        date = get_date()
        return date


class GetDbTitles:
    def execute(self, table_name:str, date: Optional[str]=None):
        titles = get_titles_from_db(table_name, date)
        return titles
        

class WriteToDataBase:
    def execute(self, scraper) -> dict:
        create_table(str(scraper))

        scraper_titles = GetAllTitles().execute(scraper)
        db_titles = GetDbTitles().execute(str(scraper), date=str(digi24.curent_date()))

        titles_not_in_db = check_if_title_in_db(scraper_titles, db_titles)

        loop_criteria = True if len(titles_not_in_db)>=1 else False

        counter = {'titles not in db': len(titles_not_in_db), 'titles in db': len(db_titles)}

        if loop_criteria is True:
            for index,title in enumerate(titles_not_in_db):
                add_title_in_db(scraper, title)
        return counter






class GetCountedWords:
    def execute(self, table_name):
        clear_screen()
        date = GetDate().execute()
        titles = GetDbTitles().execute(str(table_name), date)

        parsed_titles = parse_titles(titles)
        return (parsed_titles, date)


class PlotData:
    def execute(self, table_name):
        clear_screen()
        n = int(input('Number of words to plot: '))

        data_and_date = GetCountedWords().execute(table_name)
        data = data_and_date[0].items()
        date = data_and_date[1]

        db_date = get_date_from_db(table_name)
        
        data = (get_top_words(dict(data), n))
        plot_data(data, date, db_date)
        
