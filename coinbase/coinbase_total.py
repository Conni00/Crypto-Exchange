import requests
import time
from datetime import datetime
# Binance API Endpoint für Exchange-Informationen
api_url = "https://api.coinbase.com/api/v3/brokerage/market/products"

# Abruf aller Handelspaare
response = requests.get(api_url)
data = response.json()
time.sleep(3)
# Filter für Handelspaare, die Bitcoin (BTC) beinhalten
btc_pairs = [symbol['product_id'] for symbol in data['products'] if 'BTC' in symbol['product_id']]

# Ausgabe der BTC-Handelspaare
with open("result_coinbase_btc.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in btc_pairs:
    api_url = f"https://api.coinbase.com/api/v3/brokerage/market/products/{symbol}/ticker?limit=1000"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_coinbase_btc.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['trades']:
            f.write(f"{trade['trade_id']},{str(datetime.strptime(trade['time'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())[:10]},{trade['size']}\n")

eth_pairs = [symbol['product_id'] for symbol in data['products'] if 'ETH' in symbol['product_id']]


with open("result_coinbase_eth.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in eth_pairs:
    api_url = f"https://api.coinbase.com/api/v3/brokerage/market/products/{symbol}/ticker?limit=1000"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_coinbase_eth.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['trades']:
            f.write(f"{trade['trade_id']},{str(datetime.strptime(trade['time'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())[:10]},{trade['size']}\n")



rest_pairs = [symbol['product_id'] for symbol in data['products'] if 'BTC' not in symbol['product_id'] and 'ETH' not in symbol['product_id']]

with open("result_coinbase_Rest.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in rest_pairs:
    api_url = f"https://api.coinbase.com/api/v3/brokerage/market/products/{symbol}/ticker?limit=1000"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_coinbase_Rest.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['trades']:
            f.write(f"{trade['trade_id']},{str(datetime.strptime(trade['time'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())[:10]},{trade['size']}\n")


with open("result_coinbase_total.txt",'w') as f:
    for name in ["result_coinbase_btc.txt","result_coinbase_eth.txt","result_coinbase_Rest.txt"]:
        f.write(open(name,'r').read())
        