import requests
import json
import random
import time

# Load phrases
with open("pharse.txt", "r") as f:
    phrases = [line.strip() for line in f if line.strip()]

# Load proxies
with open("proxy.txt", "r") as f:
    proxies_list = [line.strip() for line in f if line.strip()]

# Helper: get address from seed phrase (fake example, replace if needed)
def get_wallet_address(phrase):
    # Gunakan metode real jika punya (misal: eth_account atau via API eksternal)
    # Untuk sekarang kita pakai dummy
    return "0x" + str(abs(hash(phrase)))[:40]

# Claim function
def claim_faucet(address, proxy=None):
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://faucet-miniapp.monad.xyz",
        "Referer": "https://faucet-miniapp.monad.xyz/",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "address": address
    }

    proxy_dict = {"http": proxy, "https": proxy} if proxy else None

    try:
        res = requests.post(
            "https://faucet-miniapp.monad.xyz/api/claim",
            headers=headers,
            data=json.dumps(data),
            proxies=proxy_dict,
            timeout=10
        )
        if res.status_code == 200:
            print(f"[✅] Claimed for {address}")
        else:
            print(f"[❌] Failed {address}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[⚠️] Error {address}: {e}")

# Main
for idx, phrase in enumerate(phrases):
    address = get_wallet_address(phrase)
    if idx // 3 < len(proxies_list):
        proxy = proxies_list[idx // 3]  # 3 akun per IP
    else:
        proxy = None

    print(f"[🔁] Trying: {address} with proxy: {proxy}")
    claim_faucet(address, proxy)
    time.sleep(random.uniform(1, 3))  # jeda random biar aman
