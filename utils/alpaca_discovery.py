#!/usr/bin/env python3
"""
Filename: utils/alpaca_discovery.py
Version: 0.7.5
Role: Discovery tool to sniff out seestar_alp custom actions.
Owner: Ed de la Rie (PE5ED)
"""
import requests
import json
import tomllib
from pathlib import Path

def discover():
    # Load connection info from config
    try:
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        conn = config.get("connections", {})
        host = conn.get("seestar_alp_host", "127.0.0.1")
        port = conn.get("seestar_alp_port", 11111)
    except Exception:
        host, port = "127.0.0.1", 11111

    base_url = f"http://{host}:{port}/api/v1/telescope/0"
    
    print(f"[*] Probing seestar_alp at {host}:{port}...")
    
    endpoints = [
        "supportedactions",
        "commandbool",
        "commandstring"
    ]

    for ep in endpoints:
        try:
            r = requests.get(f"{base_url}/{ep}", timeout=5)
            if r.status_code == 200:
                print(f"\n[+] Results for {ep}:")
                print(json.dumps(r.json(), indent=4))
            else:
                print(f"[-] {ep} returned status {r.status_code}")
        except Exception as e:
            print(f"[!] Error probing {ep}: {e}")

if __name__ == "__main__":
    discover()
