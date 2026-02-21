from core.aavso_client import AAVSOClient
from core.sequence_repository import SequenceRepository

def run_sync():
    print("🚀 Starting AAVSO Catalog Sync...")
    
    client = AAVSOClient()
    repo = SequenceRepository()
    
    print("📡 Fetching 'Alerts & Campaigns' targets...")
    targets = client.fetch_campaign_targets("ac")
    
    if targets:
        repo.save_targets(targets)
        print("🌟 Catalog Sync Complete. System is ready for offline autonomy.")
    else:
        print("❌ Sync failed. No targets fetched.")

if __name__ == "__main__":
    run_sync()
