"""
Filename: core/hardware_profiles.py
Objective: Define optical characteristics for the Seestar fleet.
"""

PROFILES = {
    "S50": {
        "aperture": 50,
        "focal_length": 250,
        "sensor": "IMX462",
        "fov": (1.3, 0.7),
        "resolution": (1920, 1080),
        "max_gain": 100
    },
    "S30": {
        "aperture": 30,
        "focal_length": 150,
        "sensor": "IMX662",
        "fov": (2.4, 1.3),
        "resolution": (1920, 1080),
        "max_gain": 80
    },
    "S30_PRO": {
        "aperture": 30,
        "focal_length": 160,
        "sensor": "IMX585",
        "fov": (4.3, 2.4),
        "resolution": (3840, 2160),
        "max_gain": 80
    }
}

def get_config(model_name="S30_PRO"):
    return PROFILES.get(model_name, PROFILES["S30"])
