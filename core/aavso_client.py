import requests
from .env_loader import cfg

class AAVSOClient:
    def __init__(self):
        self.api_key = cfg("AAVSO_TARGET_KEY") 
        self.target_url = "https://targettool.aavso.org/TargetTool/api/v1/targets"
        self.vsp_url = "https://apps.aavso.org/vsp/api/chart/"

    def fetch_campaign_targets(self, section="ac"):
        if not self.api_key:
            raise ValueError("❌ AAVSO_TARGET_KEY is missing from .env")
        
        params = {"obs_section": f'["{section}"]'}
        try:
            r = requests.get(self.target_url, params=params, auth=(self.api_key, "api_token"), timeout=15)
            r.raise_for_status()
            return r.json().get("targets", [])
        except requests.exceptions.RequestException as e:
            print(f"❌ AAVSO API Error: {e}")
            return []

    def fetch_sequence(self, star_name, fov=60):
        """Fetches comparison stars for the given star and extracts only V-band data."""
        params = {"star": star_name, "fov": fov, "maglimit": 14, "format": "json"}
        try:
            r = requests.get(self.vsp_url, params=params, timeout=45)
            r.raise_for_status()
            
            raw_photometry = r.json().get("photometry", [])
            cleaned_sequence = []
            
            for comp in raw_photometry:
                # Hunt through the list of bands for the 'V' band
                v_mag = None
                for band_data in comp.get("bands", []):
                    if band_data.get("band") == "V":
                        v_mag = band_data.get("mag")
                        break
                
                # Only keep comparison stars that actually have a V-band measurement
                if v_mag is not None:
                    cleaned_sequence.append({
                        "auid": comp.get("auid"),
                        "ra": comp.get("ra"),
                        "dec": comp.get("dec"),
                        "label": comp.get("label"),
                        "v_mag": v_mag
                    })
                    
            return cleaned_sequence
            
        except requests.exceptions.RequestException as e:
            print(f"❌ VSP API Error for {star_name}: {e}")
            return None
