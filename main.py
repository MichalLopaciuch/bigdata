from pymongo import MongoClient
from Scrapper import Scrapper

import utils

__filename__ = 'thomann_staff.csv'

client = MongoClient('mongodb://localhost:27017')
db = client['data']
collection = db.pages

thomann = Scrapper(collection)

# thomann.scrap('https://www.thomann.de/intl/4_string_j_basses.html?ls=100&pg=1')
# thomann.scrap('https://www.thomann.de/intl/4_string_j_basses.html?ls=100&pg=2')
# thomann.scrap('https://www.thomann.de/intl/4_string_j_basses.html?ls=100&pg=3')

thomann.extract('span', {'class': 'title__manufacturer'},
                'span', {'class': 'fx-typography-price-primary fx-price-group__primary product__price-primary'})
thomann.save(__filename__)


utils.company_freq(thomann.get_names())
utils.price_stats(__filename__)

