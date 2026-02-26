# Alpaca Bridge Implementation
The Seestar Federation utilizes a strict ASCOM Alpaca bridge on Port 5555. 
All `Action` calls (like `get_schedule`) MUST use the **PUT** method.
Mandatory parameters for every call:
- Action
- Parameters (JSON string)
- ClientID
- ClientTransactionID
