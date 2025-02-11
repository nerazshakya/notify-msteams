import json
import sys
import requests
import datetime

# Base URL for icons hosted in the GitHub repository
GITHUB_REPO_URL = "https://raw.githubusercontent.com/nerazshakya/notify-msteams/main/icons/"

def send_teams_notification(webhook_url, repo, branch, commit, actor, event, title, message, status):
    """Send an Adaptive Card message to Microsoft Teams with custom icons."""

    # Mapping status to colors and icons
    status_colors = {
        "Success": "#28a745",  # Green
        "Failure": "#dc3545",  # Red
        "Warning": "#ffc107",  # Yellow
        "Info": "#007bff",      # Blue
        "Skipped": "#6c757d",   # Gray
        "Cancelled": "#ff5733"  # Orange
    }
    
    status_icons = {
        "Success": "success.png",
        "Failure": "failure.png",
        "Warning": "unknown.png",
        "Info": "unknown.png",
        "Skipped": "skipped.png",
        "Cancelled": "cancelled.png"
    }

    icon_url = f"{GITHUB_REPO_URL}{status_icons.get(status, 'unknown.png')}"
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

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
                    "backgroundImage": {
                        "url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                    },
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
                                {"title": "Commit", "value": commit[:7]},  # Short commit hash
                                {"title": "Actor", "value": actor},
                                {"title": "Event", "value": event},
                                {"title": "Status", "value": status},
                                {"title": "Time", "value": timestamp}
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

    # Send request to Teams
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(adaptive_card), headers=headers)

    if response.status_code == 200:
        print("✅ Notification sent successfully.")
    else:
        print(f"❌ Failed to send notification: {response.text}")

if __name__ == "__main__":
    webhook_url = sys.argv[1]
    repo = sys.argv[2]   # Repository name
    branch = sys.argv[3]  # Branch name
    commit = sys.argv[4]  # Commit hash
    actor = sys.argv[5]   # GitHub actor
    event = sys.argv[6]   # GitHub event type
    title = sys.argv[7]   # Notification title
    message = sys.argv[8] # Main message
    status = sys.argv[9]  # Status

    send_teams_notification(webhook_url, repo, branch, commit, actor, event, title, message, status)
