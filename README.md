# 🔭 Seestar Organizer (v1.2.0 Garmt)

> **Objective:** Primary documentation and entry gate for the automated S30-PRO variable star observation pipeline.
> **Version:** 1.2.0 (Garmt / Pee Pastinakel)

**Automated Variable Star Observation Pipeline**

## 🏰 Architecture: The Rommeldam Federation
This project utilizes a **Modular 3-Block Architecture** to manage the lifecycle of astronomical data. Following the **Single Responsibility Principle**, all logic is partitioned into Preflight, Flight, and Post-flight pillars.

## 🧠 The ET Protocol (Logic Hub)
For technical deep-dives into our networking, state-machine logic, and AAVSO handshake protocols, see the **[Logic Directory](./logic/README.md)**.

* **[Master Workflow](./logic/WORKFLOW.md)**: The end-to-end data lifecycle.
* **[Data Mapping](./logic/data_mapping.md)**: Understanding the "Funnel" pattern.
* **[API Protocols](./logic/api_protocol.md)**: Mandatory throttling and connection rules.

## 🛫 System Entry Points
* **Setup Wizard (`setup_wizard.py`)**: The interactive CLI for initial configuration.
* **Kwetal Sentry (`main.py`)**: The primary background daemon managing hardware loops.

## 🍷 Slotwoord van een Heer van Stand
"Het is een hele zorg, nietwaar? De sterrenhemel is onmetelijk en de techniek staat voor niets... wij handelen hier volgens de regelen van het fatsoen!"
