import requests

class SeestarClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.base_url = f"http://{host}:{port}/api/v1/telescope/0"
        self.client_id = 1
        self.transaction_id = 0

    def _get_transaction_id(self):
        self.transaction_id += 1
        return self.transaction_id

    def is_connected(self):
        try:
            params = {
                "ClientID": self.client_id,
                "ClientTransactionID": self._get_transaction_id()
            }
            response = requests.get(f"{self.base_url}/connected", params=params, timeout=2)
            if response.status_code == 200:
                return response.json().get("Value", False)
            return False
        except Exception:
            return False

    def get_coordinates(self):
        try:
            params = {
                "ClientID": self.client_id,
                "ClientTransactionID": self._get_transaction_id()
            }
            ra = requests.get(f"{self.base_url}/rightascension", params=params).json().get("Value")
            dec = requests.get(f"{self.base_url}/declination", params=params).json().get("Value")
            return ra, dec
        except:
            return None, None
