"""
Filename: core/ekos.py
Version: 0.7.1
Role: Generates Ekos Scheduler List (.esl) files from priority targets.
Owner: Ed de la Rie (PE5ED)
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

class EkosBridge:
    def __init__(self, config: dict):
        self.output_path = Path("data/tonights_plan.esl")
        self.sequence_file = config.get("ekos", {}).get("sequence_file", "/home/stellarmate/sequences/aavso_standard.esq")

    def generate_esl(self, observable_targets: list):
        """
        Converts our target list into the XML format used by Ekos.
        """
        root = ET.Element("SchedulerList")
        
        for target in observable_targets[:15]: # Top 15 targets
            job = ET.SubElement(root, "Job")
            
            # Metadata
            ET.SubElement(job, "Name").text = target['name']
            ET.SubElement(job, "Group").text = "AAVSO_Science"
            ET.SubElement(job, "Priority").text = "1"
            
            # Coordinates
            coords = ET.SubElement(job, "Coordinates")
            ET.SubElement(coords, "RA").text = target['ra']
            ET.SubElement(coords, "Dec").text = target['dec']
            
            # Execution
            ET.SubElement(job, "Sequence").text = self.sequence_file
            ET.SubElement(job, "StartupCondition").text = "Now"
            ET.SubElement(job, "CompletionCondition").text = "Sequence"
            
            # Constraints
            constraints = ET.SubElement(job, "Constraints")
            ET.SubElement(constraints, "MinAltitude").text = str(target.get('min_alt', 40))
            
        # Pretty print XML
        xml_str = ET.tostring(root, encoding='utf-8')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        
        with open(self.output_path, "w") as f:
            f.write(pretty_xml)
            
        return self.output_path

if __name__ == "__main__":
    print("[*] Ekos Bridge v0.7.1 initialized.")
