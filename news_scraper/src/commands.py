
from news_scraper.src.business import (
    get_all_titles,
    get_titles_from_db,
    create_table,
    check_if_title_in_db,
    add_title_in_db,
    get_top_words,
    parse_titles,
    digi24,
    plot,
    )
from typing import Optional





class Command:
    def execute(self):
        raise NotImplementedError()


class GetAllTitles:
    def execute(self, scraper):
        extracted_titles = get_all_titles(scraper)
        return extracted_titles

    
class SearchKeyword:
    def execute(self, scraper, keyword: str):
        all_titles = GetAllTitles().execute(scraper)
        filtered_titles = []

        for title in all_titles:
            if keyword in title.lower():
                filtered_titles.append(title)
        return filtered_titles


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
    def execute(self, table_name, date):
        titles = GetDbTitles().execute(str(table_name),date)
        parsed_titles = parse_titles(titles)
        return (parsed_titles)


class PlotData:
    def execute(self, table_name, date, num_words):
        data = GetCountedWords().execute(table_name, date).items()
        if len(data) < 1:
            return f'No tites saved in date: {date}'

        data = (get_top_words(dict(data), num_words))

        plot_str = plot(data, date)
        return plot_str
