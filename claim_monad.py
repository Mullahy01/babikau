import requests
from web3 import Web3
from eth_account import Account
import random, time

def load_phrases(filename="pharse.txt"):
    return [line.strip() for line in open(filename) if line.strip()]

def load_proxies(filename="proxy.txt"):
    return [line.strip() for line in open(filename) if line.strip()]

def get_address_from_phrase(phrase):
    acct = Account.from_mnemonic(phrase)
    return acct.address

def claim(address, proxy):
    url = "https://faucet-miniapp.monad.xyz/api/claim"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://faucet-miniapp.monad.xyz",
        "referer": "https://faucet-miniapp.monad.xyz/",
        "user-agent": "Mozilla/5.0",
    }
    data = {"address": address}
    try:
        resp = requests.post(url, json=data, headers=headers, proxies={
            "http": proxy, "https": proxy
        }, timeout=15)
        print(f"[{address[:8]}] Status: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        print(f"[{address[:8]}] ERROR: {e}")

def main():
    phrases = load_phrases()
    proxies = load_proxies()
    if not phrases or not proxies:
        print("pharse.txt dan proxy.txt tidak boleh kosong!")
        return
    for i, phrase in enumerate(phrases):
        if i >= len(proxies) * 3:
            break
        proxy = proxies[i // 3]
        address = get_address_from_phrase(phrase)
        claim(address, proxy)
        time.sleep(1.5)

if __name__ == "__main__":
    main()