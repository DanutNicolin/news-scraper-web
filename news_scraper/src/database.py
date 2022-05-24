
from typing import Optional

import sqlite3
import datetime



class DataBaseManager:
    def __init__(self, db_name: str):
        db_path = 'news_scraper/src/database.db'
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def _execute(self, statement: str, values: list=[]):
        cursor = self.conn.cursor()
        cursor.execute(statement, values)
        return cursor


    def curent_date(self):
        curent_date = datetime.date.today().strftime('%d.%m.%Y')
        return str(curent_date)


    def create_table(self, table_name: str):
        self._execute(f"""CREATE TABLE IF NOT EXISTS {table_name}"""+ 
                      f"""(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, title TEXT);""")

    
    def drop_table(self, table_name: str):
        self._execute(f"""DROP TABLE {table_name};""")

    
    def add_data(self, table_name: str, data: Optional[str]=None):
        date = self.curent_date()
        values = date, data
        placeholders = ','.join('?' * len(values))

        self._execute(f"""INSERT INTO {table_name}"""+
                       """(date, title)"""+
                      f"""VALUES({placeholders});""",
                      values
                      )
        self.conn.commit()


    def retrieve_data(self, table_name: str, date: Optional[str]=None):
        query = f"""SELECT * FROM {table_name}"""
        
        if date:
            query += f""" WHERE date = ?"""
            query += f""" ORDER BY id"""
            return self._execute(query, [date]).fetchall()
        else:
            query += f""" ORDER BY id"""
            return self._execute(query).fetchall()

