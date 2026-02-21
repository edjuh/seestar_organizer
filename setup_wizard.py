import os, shutil, socket

def get_system_intel():
    intel = {'external_drives': [], 'gps': False, 'alpaca': False}
    try:
        with open("/sys/firmware/devicetree/base/model", "r") as f:
            intel['model'] = f.read().strip('\x00')
    except: intel['model'] = "StellarMate / Linux Workstation"
    
    total, used, free = shutil.disk_usage("/")
    intel['free_gb'] = round(free / (2**30), 1)
    
    for m in ['/media', '/mnt']:
        if os.path.exists(m):
            for i in os.listdir(m):
                p = os.path.join(m, i)
                if os.path.ismount(p):
                    _, _, f_e = shutil.disk_usage(p)
                    intel['external_drives'].append({'path': p, 'free': round(f_e / (2**30), 1)})
    
    intel['gps'] = any(os.path.exists(p) for p in ['/dev/ttyACM0', '/dev/ttyUSB0'])
    try:
        with socket.create_connection(("127.0.0.1", 5555), timeout=0.5): intel['alpaca'] = True
    except: pass
    return intel

def validate_input(val, default, name):
    if not val: return default
    try:
        return float(val)
    except ValueError:
        print(f"  --> [!] '{val}' is not a valid number for {name}. Using default: {default}.")
        return float(default)

def main():
    os.system('clear')
    intel = get_system_intel()
    
    print("="*70)
    print("   🔭  SEESTAR S30-PRO ORGANIZER : INITIAL CONFIGURATION")
    print("="*70)
    print("Welcome.")
    print("\nThis application is designed to transform the Seestar series into a")
    print("dedicated scientific instrument for variable star research.")
    
    print("\n[ MANDATORY PRE-FLIGHT CHECK ]")
    print("The telescope MUST be initialized first using the official Seestar app.")
    print("Ensure you have performed the initial calibration and firmware updates.")
    print("The Organizer can take command once the unit is operational on the network.")

    print("\n[ RESEARCHER NOTE ]")
    print("The developers of this suite strongly recommend participating in the")
    print("AAVSO (American Association of Variable Star Observers) community.")
    print("-" * 70)
    
    pri_def = intel['external_drives'][0]['path'] if intel['external_drives'] else "/home/stellarmate/archive"
    print(f"SYSTEM SCAN: {intel['model']} | {intel['free_gb']}GB Free")
    print(f"GPS STATUS: {'DETECTED (High-Precision Timing Enabled)' if intel['gps'] else 'NOT FOUND (Using Network Time)'}")
    print("-" * 70)

    # --- THE INTERVIEW ---
    print("\n[ PHASE 1: HARDWARE ]")
    mount = input("Mount Configuration (ALTAZ or EQ Wedge) [ALTAZ]: ").strip().upper() or "ALTAZ"
    exp = 10 if mount == "ALTAZ" else 30
    
    print(f"\n[ PHASE 2: STORAGE ]")
    print(f"Suggested archive path: {pri_def}")
    pri = input("Confirm or enter a different path: ").strip() or pri_def
    
    print("\n[ PHASE 3: OPERATION ]")
    sim = "true" if input("Enable 'Simulation Mode' for testing? (y/n) [n]: ").lower() == 'y' else "false"
    
    print("\n[ PHASE 4: SCIENTIFIC CREDENTIALS ]")
    obs = input("AAVSO Observer Code: ") or "N/A"
    w_tok = input("AAVSO WebObs Token: ") or ""
    t_tok = input("AAVSO Target Tool Key: ") or ""
    m_key = input("Meteoblue API Key (Required for safety): ") or ""
    
    print("\n[ PHASE 5: COORDINATES ]")
    print("Static fallback coordinates for Airmass/HJD calculations.")
    lat = validate_input(input("Latitude (Decimal) [52.3874]: "), "52.3874", "Latitude")
    lon = validate_input(input("Longitude (Decimal) [4.6462]: "), "4.6462", "Longitude")
    elv = validate_input(input("Elevation (Meters) [2.0]: "), "2.0", "Elevation")

    config_template = f"""[hardware]
mount_type = "{mount}"
default_exposure = {exp}

[storage]
source_dir = "/home/stellarmate/seestar_downloads"
primary_dir = "{pri}"
lifeboat_dir = "/home/stellarmate/seestar_organizer/local_buffer"

[alpaca]
host = "127.0.0.1"
port = 5555
simulate = {sim}

[aavso]
observer_code = "{obs}"
webobs_token = "{w_tok}"
target_tool_key = "{t_tok}"

[weather]
meteoblue_apikey = "{m_key}"

[location]
lat = {lat}
lon = {lon}
elevation = {elv}
"""

    if os.path.exists("config.toml"):
        if input("\n[!] A config.toml already exists. Replace it? (y/n): ").lower() != 'y':
            print("Aborted. No changes made."); return

    with open("config.toml", "w") as f: f.write(config_template)
    print("\n" + "="*70)
    print("✅ CONFIGURATION SAVED.")
    print("The S30-PRO Organizer is ready for service.")
    print("="*70 + "\n")

if __name__ == "__main__": main()
