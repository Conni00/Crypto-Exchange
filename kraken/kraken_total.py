import requests
import time
# Binance API Endpoint für Exchange-Informationen
api_url = "https://api.kraken.com/0/public/AssetPairs"

# Abruf aller Handelspaare
response = requests.get(api_url)
data = response.json()
time.sleep(3)

# Filter für Handelspaare, die Bitcoin (BTC) beinhalten
btc_pairs = [symbol for symbol in data['result'] if 'XBT' in symbol]
eth_pairs = [symbol for symbol in data['result'] if 'ETH' in symbol]
rest_pairs = [symbol for symbol in data['result'] if 'XTC' not in symbol and 'ETH' not in symbol]
# Ausgabe der BTC-Handelspaare
with open("result_kraken_btc.txt","w") as f:
    f.write("id,time,qty\n")

for symbol in btc_pairs:
    api_url = f"https://api.kraken.com/0/public/Trades?pair={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_kraken_btc.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['result'][symbol]:
            f.write(f"{trade[-1]},{str(trade[2])[:10]},{trade[3]}\n")

with open("result_kraken_eth.txt","w") as f:
    f.write("id,time,qty\n")

for symbol in eth_pairs:
    api_url = f"https://api.kraken.com/0/public/Trades?pair={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_kraken_eth.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['result'][symbol]:
            f.write(f"{trade[-1]},{str(trade[2])[:10]},{trade[3]}\n")

with open("result_kraken_Rest.txt","w") as f:
    f.write("id,time,qty\n")

for symbol in rest_pairs:
    api_url = f"https://api.kraken.com/0/public/Trades?pair={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_kraken_Rest.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['result'][symbol]:
            f.write(f"{trade[-1]},{str(trade[2])[:10]},{trade[3]}\n")

with open("result_kraken_total.txt",'w') as f:
    for name in ["result_kraken_btc.txt","result_kraken_eth.txt","result_kraken_Rest.txt"]:
        f.write(open(name,'r').read())
        