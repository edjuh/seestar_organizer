#!/usr/bin/env python3
import json
from pathlib import Path

def create_ekos_list():
    status_path = Path("logs/target_status.json")
    if not status_path.exists(): return
    
    with open(status_path, "r") as f:
        data = json.load(f)
    
    # XML structure for Ekos Scheduler
    xml = "<SchedulerList>\n"
    for t in data["observable"][:12]: # Grab the top dozen
        xml += f"""  <Job>
    <Name>{t['name']}</Name>
    <Coordinates>
      <RA>{t['ra']}</RA>
      <Dec>{t['dec']}</Dec>
    </Coordinates>
    <Sequence>/home/stellarmate/sequences/aavso_standard.esq</Sequence>
    <Priority>1</Priority>
  </Job>\n"""
    xml += "</SchedulerList>"
    
    with open("data/tonights_plan.esl", "w") as f:
        f.write(xml)
    print("Generated data/tonights_plan.esl for Ekos import.")

if __name__ == "__main__":
    create_ekos_list()
