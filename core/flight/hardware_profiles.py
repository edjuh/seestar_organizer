"""
Filename: core/hardware_profiles.py
Objective: Define sensor specs for Annie (S50), Williamina (S30-Pro), and Henrietta (S30-Pro Fast).
"""

PROFILES = {
    "WILLIAMINA": {
        "model": "S30-Pro",
        "sensor": "IMX585",
        "fov": "4.6",
        "bayer": "GRBG",
        "specialty": "High-precision Photometry",
        "max_gain": 80
    },
    "ANNIE": {
        "model": "S50",
        "sensor": "IMX462",
        "fov": "2.8",
        "bayer": "RGGB",
        "specialty": "Spectroscopy",
        "max_gain": 100
    },
    "HENRIETTA": {
        "model": "S30-Pro",
        "sensor": "IMX585",
        "fov": "4.6",
        "bayer": "GRBG",
        "specialty": "Rapid-cadence Photometry (Leavitt Laws)",
        "max_gain": 80
    }
}

def get_profile(name="WILLIAMINA"):
    return PROFILES.get(name.upper(), PROFILES["WILLIAMINA"])
