import requests
import time
# Binance API Endpoint für Exchange-Informationen
data = []
for param in ["SWAP","FUTURES","SPOT","OPTION"]:
    api_url = f"https://www.okx.com/api/v5/market/tickers?instType={param}"
    response = requests.get(api_url)
    data += response.json()['data']
    time.sleep(1)
# Filter für Handelspaare, die Bitcoin (BTC) beinhalten
print(len(data))
btc_pairs = [symbol['instId'] for symbol in data if 'BTC' in symbol['instId']]

# Ausgabe der BTC-Handelspaare
with open("result_okx_btc.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in btc_pairs:
    api_url = f"https://www.okx.com/api/v5/market/trades?instId={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_okx_btc.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['data']:
            f.write(f"{trade['tradeId']},{str(trade['ts'])[:10]},xxx\n")

eth_pairs = [symbol['instId'] for symbol in data if 'ETH' in symbol['instId']]


with open("result_okx_eth.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in eth_pairs:
    api_url = f"https://www.okx.com/api/v5/market/trades?instId={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_okx_eth.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['data']:
            f.write(f"{trade['tradeId']},{str(trade['ts'])[:10]},xxx\n")

rest_pairs = [symbol['instId'] for symbol in data if 'BTC' not in symbol['instId'] and 'ETH' not in symbol['instId'] ]
with open("result_okx_Rest.txt","w") as f:
    f.write("id,time,qty\n")
for symbol in rest_pairs:
    api_url = f"https://www.okx.com/api/v5/market/trades?instId={symbol}"
    response = requests.get(api_url)
    print(symbol)
    assert response.status_code == 200
    time.sleep(1.5)
    with open("result_okx_Rest.txt","a") as f:
        f.write(f'{"="*10}{symbol}{"="*10}\n')
        for trade in response.json()['data']:
            f.write(f"{trade['tradeId']},{str(trade['ts'])[:10]},xxx\n")


with open("result_okx_total.txt",'w') as f:
    for name in ["result_okx_btc.txt","result_okx_eth.txt","result_okx_Rest.txt"]:
        f.write(open(name,'r').read())
        