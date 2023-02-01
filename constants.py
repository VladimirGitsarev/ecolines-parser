import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

CITIES = {
    'Amsterdam': '12',
    'Apeldoorn': '812',
    'Arnhem': '185',
    'Augsburg': '206',
    'Augustow': '222',
    'Baden-Baden': '968',
    'Baranovichi': '63',
    'Bauska': '57',
    'Bayreuth': '29',
    'Berlin': '211',
    'Bialystok': '103',
    'Bielefeld': '204',
    'Bila': '963',
    'Blahovishchenske (Ulianovka)': '500',
    'Bonn': '43',
    'Braunschweig': '35',
    'Bremen': '46',
    'Brest': '635',
    'Brno': '564',
    'Bydgoszcz': '253',
    'Cheboksary': '628',
    'Chemnitz': '28',
    'Cherepovets (Bus station)': '1809',
    'Chernivtsi (rail station)': '1811',
    'Chernyakhovsk': '806',
    'Darmstadt': '295',
    'Daugavpils': '2',
    'Dnipro': '79',
    'Dortmund': '39',
    'Dresden': '27',
    'Dubno': '67',
    'Duisburg': '41',
    'Dusseldorf': '42',
    'Essen': '40',
    'Frankfurt-M': '33',
    'Freiburg': '298',
    'Fulda': '209',
    'Gdansk': '99',
    'Gdynia': '707',
    'Giessen': '309',
    'Gomel': '660',
    'Gottingen': '234',
    'Grodno': '654',
    'Groningen': '814',
    'Gusev': '805',
    'Gvardeysk': '989',
    'Hamburg': '45',
    'Hamm': '413',
    'Hannover': '36',
    'Helsinki (Airport Vantaa)': '1272',
    'Helsinki (Bus Station)': '1185',
    'Hradec-Kralove': '56',
    'Ingolstadt': '529',
    'Ivano-Frankivsk': '807',
    'Izmail': '492',
    'Jekabpils': '369',
    'Jelgava': '214',
    'Kaliningrad': '784',
    'Karlsruhe': '32',
    'Kassel': '47',
    'Katowice': '394',
    'Kaunas': '7',
    'Kazan': '612',
    'Khmelnytskyi': '929',
    'Kirishi (Bus Station)': '924',
    'Koln': '48',
    'Kolomyia': '1812',
    'Krakow': '593',
    'Kropyvnytskyi (Avtovokzal 1)': '1263',
    'Kropyvnytskyi (Tsentr)': '952',
    'Kryvyi Rih (AS 1)': '729',
    'Kutno': '1049',
    'Kyiv (Vydubychi)': '1093',
    'Kyiv (metro Teremki)': '1266',
    'Lappeenranta (Bus Station)': '1248',
    'Leipzig': '249',
    'Lida': '808',
    'Lodz': '388',
    'Lublin': '390',
    'Lutsk': '66',
    'Lviv (bus station)': '250',
    'Lviv (rail station)': '1260',
    'Lyubashivka': '501',
    'Magdeburg': '203',
    'Mannheim': '210',
    'Marijampole': '51',
    'Marijampole-DRUSK.': '520',
    'Minsk (Centralniy)': '917',
    'Mogilev': '788',
    'Moscow (Salaryevo)': '1813',
    'Moscow (Severnye Vorota)': '1257',
    'Munich': '205',
    'Munster': '38',
    'Nevel': '1782',
    'Nizhny': '675',
    'Nurnberg': '44',
    'Odessa (Starosinna)': '1094',
    'Offenburg': '315',
    'Oldenburg': '472',
    'Olomouc': '581',
    'Olsztyn': '97',
    'Opole': '726',
    'Orsha': '608',
    'Osnabruck': '37',
    'Ostrava': '580',
    'Ostrow': '228',
    'Panevezys': '50',
    'Parnu': '202',
    'Petrozavodsk': '620',
    'Petrozavodsk (Hotel Karelia)': '1270',
    'Poltava': '77',
    'Poznan': '395',
    'Prague': '565',
    'Pskov': '93',
    'Rezekne': '1324',
    'Riga (bus station)': '1',
    'Rivne': '218',
    'Rotterdam': '53',
    'Siauliai (Bus station)': '215',
    'Siauliai (Bus stop)': '1775',
    'Smolensk': '826',
    'Sofia': '182',
    'St.Petersburg (Airport Pulkovo)': '1808',
    'St.Petersburg (Moskovskaya)': '1823',
    'St.Petersburg (bus station)': '645',
    'Strasbourg': '1001',
    'Stuttgart': '31',
    'Suwalki': '221',
    'Szczecin (bus station)': '1254',
    'Tallinn (bus station)': '201',
    'Ternopil': '627',
    'The': '813',
    'Torun': '252',
    'Ulm': '207',
    'Uman': '70',
    'Utena': '220',
    'Utrecht': '52',
    'Varna': '507',
    'Vilnius': '1091',
    'Vilnius (bus station)': '6',
    'Vinnytsia': '124',
    'Vitebsk': '607',
    'Vologda (Bus Station)': '1810',
    'Warsaw 01 (Zachodnia)': '100',
    'Warsaw 02 (Centralna)': '948',
    'Wroclaw': '598',
    'Zaporizhia (Kahovska)': '1802',
    'Zaporizhia (bus station)': '80',
    'Zarasai': '115',
    'Zhytomyr': '118',
    'Zwolle': '815'
}

CURRENCIES = {
    'BYN': '26',
    'BGN': '41',
    'CZK': '32',
    'EUR': '11',
    'GBP': '9',
    'PLN': '35',
    'RUB': '12',
    'UAH': '31',
}

SEARCH_URL = 'https://booking.ecolines.net/search/result?promoCode=&currency={currency_key}&returning=0&' \
             'outwardOrigin={from_city_key}&outwardDestination={to_city_key}&outwardDate={date}&' \
             'returnOrigin={to_city_key}&returnDestination={from_city_key}&returnDate=&' \
             'adults=1&children=0&teens=0&seniors=0'

BUY_URL = 'https://ecolines.by/by/ru/booking-search?locale=ru&currency={currency_key}&returning=0&' \
          'outwardOrigin={from_city_key}&outwardDestination={to_city_key}&outwardDate={date}&' \
          'returnOrigin={to_city_key}&returnDestination={from_city_key}&returnDate=&' \
          'adults=1&children=0&teens=0&seniors=0'


EMAIL_SENDER = 'vladimir.gitsarev@gmail.com'
EMAIL_PASSWORD = 'kuzltpdithnywcvy'

BASE_DIR = os.path.dirname(__file__)

NOTIFICATION_FILE = os.path.join(BASE_DIR, 'notification.wav')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
LOGO_FILE = os.path.join(BASE_DIR, 'logo.png')
