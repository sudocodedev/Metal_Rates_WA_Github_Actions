import requests
from bs4 import BeautifulSoup

"""
Schema of gold_rates, silver_rates lists as shown below:

gold_rates = [
        [
            <Date> ,
            <Rate of 24K gold for 1gm> ,
            <Rate of 24K gold for 8gm> ,
            <Rate of 24K gold for 1gm> ,
            <Rate of 24K gold for 8gm>
        ],
        [
        ...
        ],
        ...
    ]

silver_rates = [
        [
            <Date> ,
            <Rate of silver for 1gm> ,
            <Rate of silver for 1Kg>
        ],
        [
        ...
        ],
        ...
    ]
"""

def symbols(delta:str):
    cache1,cache2 = '', ''
    if delta == '+':
        cache1 = "#00FF00"
        cache2 = "⬆"
    elif delta == '-':
        cache1 = '#FF5733'
        cache2 = '⬇'
    else:
        cache1 = '#555555'
        cache2 = '↔'
    return cache1, cache2

def price_change(rate1:str, rate2:str) -> list:
    """
        calculates the price change by comparing price of current day's with previous day's
        and returns a list which contains an emoji up (or) down (or) no change in price changes along with price diff
    """
    temp=[]
    cache1 = float(rate1.replace(',','')) - float(rate2.replace(',',''))
    cache2 = float(0)
    if cache1 == cache2: 
        temp.append('0')
        temp.append(cache1)
    else:
        if cache1 > cache2:
            temp.append('+')
            temp.append(cache1)
        else:
            temp.append('-')
            temp.append(cache1)

    return temp

def compute_rate(url:str) -> dict:
    # Returns the dictionary with required rates
    rates = {
        'date': '',
        'gold': {
            '24k': {
                '1g': '',
                '8g': '',
                'color': '',
                'symbol': '',
                'diff': ''
            },
            '22k': {
                '1g': '',
                '8g': '',
                'color': '',
                'symbol': '',
                'diff': ''
            }
        },
        'silver': {
            '1g': '',
            'color': '',
            'symbol': '',
            'diff': ''
        }
    }

    data = requests.get(url)
    
    if data.status_code != 200:
        print(f"URL responded with {data.status_code} status code...\nExiting the program...")
        exit(1)

    html = BeautifulSoup(data.text, 'html.parser')

    # Getting the respective table elements which holds required data to be fetched
    gold_elements = html.select('table.table.table-bordered.table-striped.gold-rates')[0].select("tbody")[0].select("tr")
    silver_elements = html.select('table.table.table-bordered.table-striped.silver-rates')[0].select("tbody")[0].select("tr")

    #Refer Schema for the below lists
    gold_rates = [ [ data.text.strip() for data in element.select("td") ] for element in gold_elements ]
    silver_rates = [ [ data.text.strip() for data in element.select("td") ] for element in silver_elements ]

    # Populating required values
    rates['date'] = gold_rates[0][0]
    rates['gold']['24k']['1g'] = gold_rates[0][1]
    rates['gold']['24k']['8g'] = gold_rates[0][2]
    rates['gold']['22k']['1g'] = gold_rates[0][3]
    rates['gold']['22k']['8g'] = gold_rates[0][4]
    rates['silver']['1g'] = silver_rates [0][1]

    # Calculating price change
    au1, diff1 = price_change(gold_rates[0][1],gold_rates[1][1])
    au2, diff2 = price_change(gold_rates[0][3],gold_rates[1][3])
    ag, diff3 = price_change(silver_rates[0][1], silver_rates[1][1])

    rates['gold']['24k']['diff'] = diff1
    rates['gold']['22k']['diff'] = diff2
    rates['silver']['diff'] = diff3

    rates['gold']['24k']['color'], rates['gold']['24k']['symbol'] = symbols(au1) 
    rates['gold']['22k']['color'], rates['gold']['22k']['symbol'] = symbols(au2) 
    rates['silver']['color'], rates['silver']['symbol'] = symbols(ag)

    return rates


