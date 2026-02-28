# 📡 AAVSO VSP API PROTOCOL

> **Objective:** Defines connection strings, required parameters, and mandatory throttling logic for AAVSO API interactions.
> **Version:** 1.2.0 (Garmt)

## 🔗 The Connection String
- **Canonical URL**: `https://app.aavso.org/vsp/api/chart/`
- **Method**: `GET`
- **Auth**: HTTP Basic Auth
  - **Username**: Your `AAVSO_TARGET_KEY`
  - **Password**: String literal `api_token`

## 🛠️ Required Parameters
| Parameter | Value | Purpose |
| :--- | :--- | :--- |
| `star` | Name (e.g. "CH Cyg") | Target lookup |
| `format` | `json` | Machine readable output |
| `fov` | `60` | Field of View in arcminutes |
| `maglimit` | `18.0` | Limiting magnitude for comp stars |

## ⚠️ Known Hazards
- **Caching**: Python `__pycache__` can hide URL changes. Always clear cache when modifying `aavso_client.py`.
- **400 Errors**: Usually indicate missing Auth headers or incorrect `app` subdomain.
- **Pi-Sleep**: A 188.4s delay is mandatory between successful fetches to prevent IP throttling.
