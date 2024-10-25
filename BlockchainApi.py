#BlockchainApi

import re
import argparse
import requests
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
 # Etherscan.io
    # Email:      soxem84873@rowplant.com
    # Username:   soxem84873
    # Password:   soxem84873@rowplant.com
    # Api-Key:    KW9PXSSFV2S7D7CJEUXED1MI5BPH4VZ4M1

# Funktion, um den Block für einen bestimmten Zeitstempel zu finden

def read_addresses(file_path):
    """Liest die Adressen aus der Datei, jede Adresse ist auf einer neuen Zeile."""
    with open(file_path, 'r') as file:
        addresses = [line.strip() for line in file if line.strip()]
    return addresses
def get_block_by_timestamp(timestamp, api_key):
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'block',
        'action': 'getblocknobytime',
        'timestamp': timestamp,
        'closest': 'before',
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == '1':
        return int(data['result'])
    else:
        print(f"Fehler beim Abrufen des Blocks: {data['message']}")
        return None

# Funktion, um Transaktionen der letzten 48 Stunden für eine Ethereum-Adresse abzurufen
def get_eth_transactions(address, api_key,start_block=None):
    # Etherscan API-Endpunkt für Transaktionen
    url = "https://api.etherscan.io/api"
    
    # Zeitstempel für den Startzeitpunkt (48 Stunden zurück)
    end_time = int(time.time())  # Aktuelle Zeit (Unix-Timestamp)
    start_time = end_time - 24 * 60 * 60  # 48 Stunden zurück
    
    # Abrufen der Start- und Endblöcke für den Zeitraum
    if not start_block:
        start_block = get_block_by_timestamp(start_time, api_key)
    end_block = get_block_by_timestamp(end_time, api_key)
    
    if start_block is None or end_block is None:
        print("Fehler beim Abrufen der Blocknummern.")
        return []
    
    # API-Parameter
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': start_block,
        'endblock': end_block,
        'sort': 'asc',
        'apikey': api_key
    }

    # API-Aufruf
    while True:
        try:
            response = requests.get(url, params=params)
            print(response.request.url)
            break
        except TimeoutError:
            time.sleep(5)
            continue

    # API-Ergebnis in JSON umwandeln
    data = response.json()

    # Überprüfen, ob die Anfrage erfolgreich war
    if data['status'] == '1':
        transactions = data['result']
        if len(transactions) == 10000:
            time.sleep(1)
            return transactions + get_eth_transactions(address,api_key,data['result'][9999]['blockNumber'])
        else:
            return transactions
        # Schreiben der Transaktionen in eine Datei
    else:
        print(f"Fehler bei der API-Anfrage: {data['message']}")
        return []
def get_btc_transactions(address,offset=0):
    # Blockchain.com API-Endpunkt für Bitcoin-Transaktionen einer Adresse
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}?offset={offset}"
    print("url",url)
    # API-Aufruf
    response = requests.get(url)
    
    # API-Ergebnis in JSON umwandeln
    if response.status_code == 200:
        data = response.json()

        # Überprüfen, ob Transaktionen vorhanden sind
        if 'txrefs' in data:
            transactions = data['txrefs']
            # Zeitstempel für den Startzeitpunkt (24 Stunden zurück)
            end_time = int(time.time())  # Aktuelle Zeit (Unix-Timestamp)
            start_time = end_time - 24 * 60 * 60  # 24 Stunden zurück

            # Filtern der Transaktionen nach Datum (letzte 24 Stunden)
            recent_transactions = [
                {
                    'hash': tx['tx_hash'],
                    'timeStamp': datetime.timestamp(datetime.fromisoformat(tx['confirmed'])),  # Unix-Zeitstempel
                    'value': tx['value']  # Gesamtwert der Transaktion in Satoshis
                }
                for tx in transactions if start_time <= datetime.timestamp(datetime.fromisoformat(tx['confirmed'])) <= end_time
            ]
            if len(recent_transactions) == 200 and data["hasMore"]:
                time.sleep(2)
                return recent_transactions.append(get_btc_transactions(address,offset+200))
            else: 
                return recent_transactions
        else:
            print("Keine Transaktionen gefunden.")
            return []
    else:
        print(f"Fehler bei der API-Anfrage: {response.status_code}")
        return []

def create_boxplot(file):
    with open(file,"r") as f:
        sequences = re.split(r'={10}.*={10}\n',f.read())
        timestamps = []
        time_intervals = []
        number_of_tx_and_time = [] ## (transactions, time)
        c= 0
        for sequence in sequences:
            tmp = []
            lines = sequence.split("\n")
            for line in lines:
                
                try:
                    timestamp = line.split(',')[1]
                except:
                    continue
                if timestamp[:4] == "1729" and timestamp.isdigit():
                    tmp.append(timestamp)
            if tmp: 
                time_intervals.append(int(max(tmp))-int(min(tmp)))
                number_of_tx_and_time.append((len(tmp),max(int(max(tmp))-int(min(tmp)),1)))
            timestamps += tmp
        print(max(timestamps),min(timestamps))
        len_timestamp = len(timestamps)
        interval = time_intervals[len(time_intervals)//2]
        print("Zeitinterval:",interval, 'TPS:', len(timestamps)/interval)
        print('kürzeste:',min(time_intervals), 'TPS:', min(number_of_tx_and_time, key=lambda x: x[1])[0]/min(number_of_tx_and_time, key=lambda x: x[1])[1])
        print('längste:',max(time_intervals), 'TPS:', max(number_of_tx_and_time, key=lambda x: x[1])[0]/max(number_of_tx_and_time, key=lambda x: x[1])[1])
        transaction_counts = Counter(timestamps)
        transaction_counts_full = my_copy = {key: value for key, value in transaction_counts.items()}
        for x in range(interval - len_timestamp):
            transaction_counts_full[x] = 0
        print("TPS Peak:", max(list(transaction_counts.values())))
        plt.figure(figsize=(8,6))
        sns.boxplot(data=list(transaction_counts.values()))
        plt.title("Verteilung der Transaktionen pro Sekunde")
        plt.ylabel("Transaktionen pro Sekunde")
        plt.show()

        plt.figure(figsize=(8,6))
        sns.boxplot(data=list(transaction_counts_full.values()))
        plt.title("Verteilung der Transaktionen pro Sekunde ('mit allen Sekunden')")
        plt.ylabel("Transaktionen pro Sekunde")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skript zur Verarbeitung von Blockchain-Adressen und Zeiträumen.")
    # Parameter hinzufügen
    parser.add_argument('-f', '--file', type=str, help="Pfad zur Datei, die die Adressen enthält (eine pro Zeile) [ETH\\t0xaddress].")
    parser.add_argument('-o','--output',type=str)
    parser.add_argument('-p','--plot',type=str,help="create boxplot diagram from this file")
    # Argumente parsen
    args = parser.parse_args()

    if args.file:
        addresses = read_addresses(args.file)

    # Ausgabe der eingelesenen Werte

    api_key_eth = "KW9PXSSFV2S7D7CJEUXED1MI5BPH4VZ4M1"  # Etherscan API-Schlüssel hier einfügen
    counter = 0
    if args.output:
        with open(args.output, 'w') as f:
            f.write("hashes, timestamp, value")
        for tmp in addresses:
            blockchain, address = tmp.split("\t")
            print("="*20,blockchain,address,"="*20)
            if blockchain == "ETH":
                transactions = get_eth_transactions(address, api_key_eth)
            elif blockchain == "BTC":
                time.sleep(3)
                transactions = get_btc_transactions(address)
            
            with open(args.output, 'a') as f:
                f.write(f"{'='*20}{address}{'='*20}\n")
                for tx in transactions:
                    f.write(f"{tx['hash']},{tx['timeStamp']}, {tx['value']}\n")
                # Ausgabe der Anzahl der Transaktionen
                print(f"Gefundene Transaktionen in den letzten 24 Stunden: {len(transactions)}")
            counter += len(transactions)
            print("Total Transactions:",counter)
            print("TPS:",counter/(24*60*60))
            time.sleep(0.5)
        print("Total Transactions:",counter)
        print("TPS:",counter/(24*60*60))

    if args.plot:
        create_boxplot(args.plot)
    
    
    
    
    
    
    

    # Ausgabe der Transaktionen