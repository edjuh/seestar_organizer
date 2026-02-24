"""
Filename: setup_wizard.py
Purpose: CLI interview to generate a perfect config.toml for beta testers.
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

    # --- 1. HARDWARE ---
    print("\n[ HARDWARE CONFIGURATION ]")
    print("Are you using the Seestar on a standard Tripod (AltAz) or an Equatorial Wedge (EQ)?")
    print("  Note: AltAz limits exposures to 10s to prevent field rotation.")
    mount_type = ask("Mount Type (ALTAZ / EQ)", "ALTAZ").upper()
    config["hardware"]["mount_type"] = mount_type
    
    if mount_type == "ALTAZ":
        config["hardware"]["default_exposure"] = 10
        print("  -> Exposure limit safely locked to 10 seconds.")
    else:
        exp = ask("Max Exposure Time in seconds", "30")
        config["hardware"]["default_exposure"] = int(exp)

    # --- 2. STORAGE ---
    print("\n[ STORAGE & ARCHIVE ]")
    config["storage"]["source_dir"] = ask("Downloads directory (from Seestar)", "/home/stellarmate/seestar_downloads")
    config["storage"]["primary_dir"] = ask("NAS or USB Archive directory", "/mnt/astro_nas/organized_fits")
    config["storage"]["lifeboat_dir"] = ask("Local fallback directory", "/home/stellarmate/seestar_organizer/local_buffer")

    # --- 3. ALPACA & NETWORK ---
    print("\n[ NETWORK & MIDDLEWARE ]")
    print("If running seestar_alp on this StellarMate, leave as 127.0.0.1")
    config["alpaca"]["host"] = ask("Alpaca API IP Address", "127.0.0.1")
    config["alpaca"]["port"] = int(ask("Alpaca API Port", "5555"))
    sim_ans = ask("Simulate Hardware for testing? (y/n)", "n").lower()
    config["alpaca"]["simulate"] = True if sim_ans == 'y' else False

    # --- 4. AAVSO ---
    print("\n[ SCIENCE & AAVSO ]")
    config["aavso"]["observer_code"] = ask("AAVSO Observer Code (Leave blank if none)", "")

    # --- 5. LOCATION (Fallback) ---
    print("\n[ LOCATION FALLBACK ]")
    print("If your GPS dongle fails, we need static coordinates for HJD/Airmass math.")
    config["location"]["lat"] = float(ask("Latitude (Decimal)", "52.3874"))
    config["location"]["lon"] = float(ask("Longitude (Decimal)", "4.6462"))
    config["location"]["elevation"] = float(ask("Elevation in meters", "2.0"))

    # --- GENERATE TOML ---
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
    print("You can now start the Autonomy Engine.")
    print("="*60)

if __name__ == "__main__":
    main()
