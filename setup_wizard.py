#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: setup_wizard.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Interactive CLI for configuring GPS coordinates, weather APIs, Alpaca bridge parameters, and AAVSO credentials.
"""

import os
import tomllib

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask(question, default=None):
    prompt = f"{question} [{default}]: " if default else f"{question}: "
    answer = input(prompt).strip()
    return answer if answer else default

def main():
    clear_screen()
    print("="*60)
    print(" 🔭 S30-PRO AUTONOMY : SETUP WIZARD")
    print("="*60)
    print("Welcome! This wizard will configure your Seestar array.")
    print("Press ENTER to accept the default values in brackets.\n")

    config = {"hardware": {}, "storage": {}, "alpaca": {}, "aavso": {}, "location": {}}

    print("\n[ HARDWARE CONFIGURATION ]")
    mount_type = ask("Mount Type (ALTAZ / EQ)", "ALTAZ").upper()
    config["hardware"]["mount_type"] = mount_type
    
    if mount_type == "ALTAZ":
        config["hardware"]["default_exposure"] = 10
        print("  -> Exposure limit safely locked to 10 seconds.")
    else:
        exp = ask("Max Exposure Time in seconds", "30")
        config["hardware"]["default_exposure"] = int(exp)

    print("\n[ STORAGE & ARCHIVE ]")
    config["storage"]["source_dir"] = ask("Downloads directory (from Seestar)", "/home/stellarmate/seestar_downloads")
    config["storage"]["primary_dir"] = ask("NAS or USB Archive directory", "/mnt/astro_nas/organized_fits")
    config["storage"]["lifeboat_dir"] = ask("Local fallback directory", "/home/stellarmate/seestar_organizer/local_buffer")

    print("\n[ NETWORK & MIDDLEWARE ]")
    config["alpaca"]["host"] = ask("Alpaca API IP Address", "127.0.0.1")
    config["alpaca"]["port"] = int(ask("Alpaca API Port", "5555"))
    sim_ans = ask("Simulate Hardware for testing? (y/n)", "n").lower()
    config["alpaca"]["simulate"] = True if sim_ans == 'y' else False

    print("\n[ SCIENCE & AAVSO ]")
    config["aavso"]["observer_code"] = ask("AAVSO Observer Code (Leave blank if none)", "")

    print("\n[ LOCATION FALLBACK ]")
    config["location"]["lat"] = float(ask("Latitude (Decimal)", "52.3874"))
    config["location"]["lon"] = float(ask("Longitude (Decimal)", "4.6462"))
    config["location"]["elevation"] = float(ask("Elevation in meters", "2.0"))

    print("\nGenerating config.toml...")
    
    toml_content = ""
    for section, keys in config.items():
        toml_content += f"[{section}]\n"
        for k, v in keys.items():
            if isinstance(v, str):
                toml_content += f'{k} = "{v}"\n'
            elif isinstance(v, bool):
                toml_content += f'{k} = {"true" if v else "false"}\n'
            else:
                toml_content += f'{k} = {v}\n'
        toml_content += "\n"

    with open("config.toml", "w") as f:
        f.write(toml_content)

    print("✅ SUCCESS! config.toml has been written.")
    print("="*60)

if __name__ == "__main__":
    main()
