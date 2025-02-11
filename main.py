import json
import requests
import os

def send_teams_notification():
    webhook_url = os.getenv('INPUT_WEBHOOK_URL')
    title = os.getenv('INPUT_TITLE', 'GitHub Action Notification')
    message = os.getenv('INPUT_MESSAGE')
    theme_color = os.getenv('INPUT_THEME_COLOR', '0076D7')

    if not webhook_url or not message:
        raise ValueError("Missing required inputs: 'webhook_url' and 'message'.")

    card = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "themeColor": theme_color,
        "summary": title,
        "sections": [{
            "activityTitle": f"**{title}**",
            "text": message,
            "markdown": True
        }]
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(card))

    if response.status_code == 200:
        print("✅ Notification sent successfully!")
    else:
        print(f"❌ Failed to send notification: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_teams_notification()
