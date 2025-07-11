
import os
import time
import requests

TG_TOKEN = os.getenv("BOT_TOKEN")
TG_CHAT_ID = os.getenv("CHAT_ID")
ETH_ADDRESSES = os.getenv("ETH_ADDRESS", "").split(",")
TRON_ADDRESSES = os.getenv("TRON_ADDRESS", "").split(",")
BTC_ADDRESSES = os.getenv("BTC_ADDRESS", "").split(",")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def send_message(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def get_price(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
        return float(r["price"])
    except:
        return 0

def get_latest_eth_tx(address):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    try:
        r = requests.get(url).json()
        txs = r.get("result", [])
        for tx in txs:
            if tx["to"].lower() == address.lower():
                return tx
    except:
        pass
    return None

def get_latest_tron_tx(address):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20?limit=5"
    try:
        r = requests.get(url).json()
        txs = r.get("data", [])
        for tx in txs:
            if tx["to"] == address:
                return tx
    except:
        pass
    return None

def get_latest_btc_tx(address):
    url = f"https://blockchain.info/rawaddr/{address}"
    try:
        r = requests.get(url).json()
        txs = r.get("txs", [])
        for tx in txs:
            for out in tx["out"]:
                if out.get("addr") == address:
                    return tx
    except:
        pass
    return None

def main():
    last_seen = {}
    while True:
        eth_price = get_price("ETHUSDT")
        btc_price = get_price("BTCUSDT")

        for eth in ETH_ADDRESSES:
            eth = eth.strip()
            tx = get_latest_eth_tx(eth)
            if tx and tx["hash"] != last_seen.get(eth):
                value_eth = int(tx["value"]) / 1e18
                usd = value_eth * eth_price
                msg = f"[ETH] 入金\n客户地址: {tx['from']}\n我们地址: {tx['to']}\n💰 {value_eth:.6f} ETH ≈ ${usd:,.2f}"
                send_message(msg)
                last_seen[eth] = tx["hash"]

        for tron in TRON_ADDRESSES:
            tron = tron.strip()
            tx = get_latest_tron_tx(tron)
            if tx and tx["transaction_id"] != last_seen.get(tron):
                val = int(tx["value"]) / (10**int(tx["token_info"]["decimals"]))
                symbol = tx["token_info"]["symbol"]
                msg = f"[TRC20] 入金\n客户地址: {tx['from']}\n我们地址: {tx['to']}\n💰 {val} {symbol}"
                send_message(msg)
                last_seen[tron] = tx["transaction_id"]

        for btc in BTC_ADDRESSES:
            btc = btc.strip()
            tx = get_latest_btc_tx(btc)
            if tx and tx["hash"] != last_seen.get(btc):
                total = sum([out["value"] for out in tx["out"] if out.get("addr") == btc]) / 1e8
                usd_val = total * btc_price
                from_addr = tx.get("inputs", [{}])[0].get("prev_out", {}).get("addr", "不明")
                msg = f"[BTC] 入金\n客户地址: {from_addr}\n我们地址: {btc}\n💰 {total:.8f} BTC ≈ ${usd_val:,.2f} USD\nTXID: {tx['hash']}"
                send_message(msg)
                last_seen[btc] = tx["hash"]

        time.sleep(5)

if __name__ == "__main__":
    main()
