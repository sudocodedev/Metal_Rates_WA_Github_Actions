import requests
import os
from bs4 import BeautifulSoup
from twilio.rest import Client

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


def price_change(rate1:str, rate2:str):
    """
        calculates the price change by comparing price of current day's with previous day's
        and returns an emoji up (or) down (or) no change in price changes
    """
    cache1 = float(rate1.replace(',','')) - float(rate2.replace(',',''))
    cache2 = float(0)
    if cache1 == cache2: return '↔️'
    return '⬆️' if cache1 > cache2 else '⬇️' 

if __name__ == "__main__":

    data = requests.get(os.environ['URL'].strip())

    html = BeautifulSoup(data.text, 'html.parser')

    # Getting the respective table elements which holds required data to be fetched
    gold_elements = html.select('table.table.table-bordered.table-striped.gold-rates')[0].select("tbody")[0].select("tr")
    silver_elements = html.select('table.table.table-bordered.table-striped.silver-rates')[0].select("tbody")[0].select("tr")

    #Refer Schema for the below lists
    gold_rates = [ [ data.text.strip() for data in element.select("td") ] for element in gold_elements ]
    silver_rates = [ [ data.text.strip() for data in element.select("td") ] for element in silver_elements ]

    #Message format
    message = f"""
    *Hi / வணக்கம்* 👋

    சென்னை  Metal Rates *{gold_rates[0][0]}*
    🪙 *Gold*
    *24K*   {price_change(gold_rates[0][1],gold_rates[1][1])}
    1g *⟶* ₹{gold_rates[0][1]}
    8g *⟶* ₹{gold_rates[0][2]}

    *22K*   {price_change(gold_rates[0][3],gold_rates[1][3])}
    1g *⟶* ₹{gold_rates[0][3]}
    8g *⟶* ₹{gold_rates[0][4]}

    🔘 *Silver*
    1g *⟶* ₹{silver_rates[0][1]}   {price_change(silver_rates[0][1], silver_rates[1][1])}
    """
    
    #Sending SMS to the respective number over WA
    client = Client(os.environ["ACCOUNT_SID"].strip(), os.environ["AUTH_TOKEN"].strip())
    message = client.messages.create(to=os.environ["TO_PHONE_NUMBER"].strip(), from_=os.environ["FROM_PHONE_NUMBER"].strip(), body=message)
    print(message.sid)
