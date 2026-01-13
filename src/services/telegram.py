import requests
import logging

class TelegramService:
    def __init__(self):
        self.token = "YOUR_TOKEN"
        self.chat_id = "YOUR_CHAT_ID"
    
    def send_notification(self, message: str):
        if "YOUR_" in self.token:
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.chat_id, "text": message})
        except Exception:
            pass
