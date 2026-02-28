# Alpaca Bridge Implementation

> **Objective:** Mandates the communication protocol for Port 5555 telescope orchestration, requiring strict PUT method usage.
> **Version:** 1.2.0 (Garmt)

The Seestar Federation utilizes a strict ASCOM Alpaca bridge on Port 5555. 
All `Action` calls (like `get_schedule`) MUST use the **PUT** method.

Mandatory parameters for every call:
- Action
- Parameters (JSON string)
- ClientID
- ClientTransactionID
