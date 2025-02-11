import json
import sys
import requests

def send_teams_notification(webhook_url, title, message, status):
    """Send an Adaptive Card message to Microsoft Teams via webhook."""
    
    colors = {
        "Success": "good",
        "Failure": "attention",
        "Warning": "warning",
        "Info": "default"
    }

    adaptive_card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ],
                    "backgroundColor": colors.get(status, "default")
                }
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(adaptive_card), headers=headers)

    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.text}")

if __name__ == "__main__":
    webhook_url = sys.argv[1]
    title = sys.argv[2] or "GitHub Notification"
    message = sys.argv[3]
    status = sys.argv[4] or "Info"

    send_teams_notification(webhook_url, title, message, status)
