from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class Alert(BaseModel):
    message: str 
    symbole: str
    price: float

@app.post('/alert')

def receive_alert(alert: Alert):
    print(alert.message)
    print(alert.symbole)
    return {'status':'Alert received'}

#FastAPI Endpoint for fetching the fundingrate
url_fundingserver = 'https://fapi.binance.com/fapi/v1/fundingRate'

def get_fundingrate(symbol: str):
     params = {'symbol': symbol}
     response_funding_server = requests.get(url_fundingserver, params=params)
     data_fundingserver = response_funding_server.json()

     if isinstance(data_fundingserver, list):
         last_fundingrate_server = data_fundingserver[-1]
         return{
                'symbol': last_fundingrate_server['symbol'],
                'fundingRate': float(last_fundingrate_server['FundinRate']),
                
           }     

     return{'Error': "no {'fundingRate'} key found in the responce."}

@app.get('/fundingRate/{symbol}')
def fetch_fundingrate(symbol: str):
     return get_fundingrate(symbol.upper())
