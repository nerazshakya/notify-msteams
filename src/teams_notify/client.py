import os
import json
import argparse
import requests
from typing import Dict, Any, Optional
from .templates import CardTemplate

class TeamsNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.templates = CardTemplate()

    def send_notification(
        self,
        message: str,
        title: str = "Notification",
        card_type: str = "basic"
    ) -> requests.Response:
        """Send notification to Teams channel"""
        card_data = self.templates.get_template(
            card_type,
            title=title,
            message=message
        )
        
        response = requests.post(
            self.webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(card_data)
        )
        response.raise_for_status()
        return response

def main():
    parser = argparse.ArgumentParser(description="Send Teams notification")
    parser.add_argument("--title", required=True, help="Card title")
    parser.add_argument("--message", required=True, help="Message content")
    parser.add_argument("--type", default="basic", help="Card template type")
    
    args = parser.parse_args()
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    
    if not webhook_url:
        raise ValueError("TEAMS_WEBHOOK_URL environment variable is required")
    
    notifier = TeamsNotifier(webhook_url)
    notifier.send_notification(
        message=args.message,
        title=args.title,
        card_type=args.type
    )

if __name__ == "__main__":
    main()