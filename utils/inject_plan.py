"""
Filename: utils/inject_plan.py
Version: 0.7.1
Role: Generates and immediately injects the .esl into StellarMate.
"""
import subprocess
from pathlib import Path

def deploy():
    # 1. Generate the plan
    print("[*] Generating local plan...")
    subprocess.run(["python3", "utils/build_tonights_plan.py"])
    
    plan_file = Path("data/tonights_plan.esl")
    if not plan_file.exists():
        print("[FAIL] Plan generation failed.")
        return

    # 2. Inject via REST API
    print("[*] Injecting plan into StellarMate Scheduler...")
    url = "http://stellarmate.local:5432/0/schedule/load"
    
    try:
        # Using curl via subprocess for sysadmin reliability
        cmd = ["curl", "-s", "-X", "POST", "-F", f"file=@{plan_file}", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Plan injected successfully. Check your Scheduler tab!")
        else:
            print(f"[FAIL] Injection error: {result.stderr}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == "__main__":
    deploy()
