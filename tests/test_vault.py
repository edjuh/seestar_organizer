from core.vault_manager import vault_manager

targets = [
    {"name": "MU Cam", "ra": "03:53:18", "dec": "+62:11:48"},
    {"name": "SS Cyg", "ra": "21:42:45", "dec": "+43:35:08"},
    {"name": "Algol",  "ra": "03:08:10", "dec": "+40:57:20"},
    {"name": "RR Lyr", "ra": "19:22:33", "dec": "+42:47:03"}
]

print(f"{'TARGET':<12} | {'ALTITUDE':<10} | {'STATUS'}")
print("-" * 40)

for t in targets:
    alt, can_see = vault_manager.get_target_visibility(t['ra'], t['dec'])
    status = "🔭 GO" if can_see else "❌ BELOW 30°"
    print(f"{t['name']:<12} | {alt:>8}° | {status}")
