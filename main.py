import json
import requests
import os

# GitHub Raw URL for hosting icons
GITHUB_ICONS_URL = "https://raw.githubusercontent.com/nerazshakya/notify-msteams/main/icons/"

# Status-based icons mapping
STATUS_ICONS = {
    "Success": "success.png",
    "Failure": "failure.png",
    "Skipped": "skipped.png",
    "Cancelled": "cancelled.png",
    "Unknown": "unknown.png"
}

def send_teams_notification():
    """Send an Adaptive Card notification to Microsoft Teams."""
    
    # Read environment variables from GitHub Actions
    webhook_url = os.getenv('INPUT_WEBHOOK_URL')
    title = os.getenv('INPUT_TITLE', 'GitHub Action Notification')
    message = os.getenv('INPUT_MESSAGE')
    status = os.getenv('INPUT_STATUS', 'Unknown')  # Expected: Success, Failure, Skipped, Cancelled, etc.
    repo = os.getenv('GITHUB_REPOSITORY', 'Unknown Repo')
    branch = os.getenv('GITHUB_REF_NAME', 'Unknown Branch')
    commit = os.getenv('GITHUB_SHA', 'Unknown')[:7]  # Short commit hash
    actor = os.getenv('GITHUB_ACTOR', 'Unknown User')
    event = os.getenv('GITHUB_EVENT_NAME', 'Unknown Event')

    # Ensure required variables are provided
    if not webhook_url or not message:
        raise ValueError("❌ Missing required inputs: 'INPUT_WEBHOOK_URL' and 'INPUT_MESSAGE'.")

    # Select the correct icon for the status
    icon_url = f"{GITHUB_ICONS_URL}{STATUS_ICONS.get(status, 'unknown.png')}"

    # Construct Adaptive Card JSON
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
                            "type": "Image",
                            "url": icon_url,
                            "size": "Medium",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Large",
                            "color": "Accent",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True,
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "Repository", "value": repo},
                                {"title": "Branch", "value": branch},
                                {"title": "Commit", "value": commit},
                                {"title": "Actor", "value": actor},
                                {"title": "Event", "value": event},
                                {"title": "Status", "value": status}
                            ]
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "View Commit",
                            "url": f"https://github.com/{repo}/commit/{commit}"
                        }
                    ]
                }
            }
        ]
    }

    # Send request to Teams Webhook
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(adaptive_card))

    if response.status_code == 200:
        print("✅ Notification sent successfully!")
    else:
        print(f"❌ Failed to send notification: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_teams_notification()
