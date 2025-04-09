from fastapi import FastAPI
import requests
import json 

app = FastAPI()

#fetching current BTC price from binance 
url= "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
response = requests.get(url)

if response.status_code == 200:
 data = response.json()
 if 'price' in data:
       btc_price = float(data['price'])
       print(f'current BTC price is: ${btc_price:,.2f}')
 else:
       print("Error: 'price' key not found in the response.")

else:
 print(f"Error: Faild to fetch BTC price status code: {response.status_code}")



#fetching fundingrate from binance 
url2 = "https://fapi.binance.com/fapi/v1/fundingRate"
params = {"symbol": 'BTCUSDT'}
response_fundingrate = requests.get(url2,params=params)

if response_fundingrate.status_code == 200:
 try:
      data_fundingrate = response_fundingrate.json()
      # assuming the fundingrate is stored under the key 'fundingRate'
      if data_fundingrate:
           last_fundingrate = data_fundingrate[-1]
           print('Last fundingrate:', last_fundingrate)
           if 'fundingRate' in last_fundingrate:
                funding_rate = float(last_fundingrate['fundingRate'])
                print(f'Fundingrate Binance: {funding_rate * 100:.4f}%')
           else:
                 print("Error: 'fundingRate' key not found in the response.")
      else: 
          print('Error: No data found in the response')
 except json.JSONDecodeError:
     print ("Error: Failed to parse JSON response for funding rate.")
else:
     print(f'Error: Failed to fetch funding rate. Status code: {response_fundingrate.status_code}')



#understanding what is given under the Market status 
url3 = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
response_marketststus = requests.get(url3)
market_data = response_marketststus.json()
print('Market status response:', market_data)

# feching the market buy and sell order number 
url4 = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
response_marketorder = requests.get(url4)
market_sellbuy = response_marketorder.json()
print('Market order response:', market_sellbuy)

if 'volume' in market_sellbuy:
 total_volume = float(market_sellbuy['volume'])
 print(f'Total volume: {total_volume}BTC')
else:
     print("Error: 'takerBuyBaseAssetVolume' or 'volume' key is not found in market_sellbuy response.")




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
