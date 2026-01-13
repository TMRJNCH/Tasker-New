import requests
import logging

class TelegramService:
    def __init__(self):
        self.token = "6248133659:AAH5MdnQbbtfhRj3MbRzSGmmKFg73xhN08Q"
        self.chat_id = "365401498"
    
    def send_notification(self, message: str):
        if "YOUR_" in self.token:
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.chat_id, "text": message})
        except Exception:
            pass
