from bs4 import BeautifulSoup
import datetime
import requests




  
class Digi24:
    def __init__(self):
        self.url = 'https://www.digi24.ro/ultimele-stiri'
        self.name = 'Digi24'

    def soup(self):
        html_text = requests.get(self.url).text
        soup = BeautifulSoup(html_text, 'lxml')
        return soup

    def curent_date(self):
        curent_date = datetime.date.today().strftime('%d.%m.%Y')
        return curent_date

    def articles_date(self):
        dates = self.soup().find_all('p', class_='article-date')
        stripped_dates = []

        for date in dates:
            date = date.span.text.lstrip()[0:10]
            stripped_dates.append(date)
        return stripped_dates

    def scrape_titles(self):
        article_dates = self.articles_date()
        titles = self.soup().find_all('h2', class_= 'article-title')
        all_articles = []

        for (title,date) in zip(titles, article_dates):
            counter = 0
            if article_dates[counter] == self.curent_date():
                counter += 1
                all_articles.append(title.text)

        return all_articles

    def __str__(self):
        return self.name

