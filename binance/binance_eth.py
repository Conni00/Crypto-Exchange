import requests
import time
# Binance API Endpoint für Exchange-Informationen
api_url = "https://api.binance.com/api/v3/exchangeInfo"

# Abruf aller Handelspaare
response = requests.get(api_url)
data = response.json()
time.sleep(3)
# Filter für Handelspaare, die Bitcoin (BTC) beinhalten
eth_pairs = [symbol['symbol'] for symbol in data['symbols'] if 'ETH' in symbol['symbol']]

# Ausgabe der BTC-Handelspaare
with open("result_binance_eth.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in eth_pairs:
    api_url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=1000"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_binance_eth.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json():
            f.write(f"{trade['id']},{str(trade['time'])[:10]},{trade['qty']}\n")

