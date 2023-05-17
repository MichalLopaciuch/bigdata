from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, collection, debug=None):
        self.collection = collection
        self.debug = debug

    def scrap(self, url):
        print(f'Scrapping {url}')
        driver = webdriver.Safari()
        driver.get(url)
        content = driver.page_source

        self.__log__(content[:10]);
        self.soup = BeautifulSoup(content, 'html.parser')
        self.__log__(bool(self.soup));
        title = self.soup.find_all('title')[0].get_text() or ''
        self.__log__(title);
        
        page = {
            'url': url,
            'content': content,
            'date': datetime.now(),
            'title': title
        }

        self.__log__(f'Trying to save {url}')
        self.__save_to_db__(page)

    def extract(self, elem1, by1, elem2, by2):
        print("Extracting")
        if not hasattr(self, 'soup'):
            print('Soup is not defined. Collecting from database...')
            content = ''
            cursor = self.collection.find({})
            for document in cursor:
                content += document.get('content')
            self.soup = BeautifulSoup(content, 'html.parser')
            print('Soup defined from database')

        self.names = self.soup.findAll(elem1, by1)
        self.data = self.soup.findAll(elem2, by2)

        self.__log__(self.names)
        self.__log__(self.data)

        for n,d in zip(self.names, self.data):
            self.__log__(f'{n.text.strip()} {d.text.strip()}')    

    def save(self, filename):
        if not hasattr(self, 'names') or not hasattr(self, 'data'):
            print('Critical error: No data - Call extract(p1, b1, p2, b2) first')
            exit(1)

        print(f"Saving {filename}")
        with open(filename, 'w') as f:
            lines = []
            for n, d in zip(self.names, self.data):
                d = d.text.strip().replace(',', '').replace('zł', '')
                lines.append(n.text.strip()+';'+d+'\n')
            if len(lines) > 0:
                lines[-1] = lines[-1].replace('\n', '')
            f.writelines(lines)

    def get_names(self):
        return [n.text for n in self.names]

    def __save_to_db__(self, item):
        response = self.collection.insert_one(item)
        self.__log__(response.inserted_id)
        print(f'{response.inserted_id} inserted')

    def __log__(self, message):
        if self.debug:
            print(self._log_counter, message)
            self._log_counter += 1

    _log_counter = 1
