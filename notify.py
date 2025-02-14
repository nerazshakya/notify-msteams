import json
import requests
import os
import pytz
import datetime
# GitHub Raw URL for hosting icons
GITHUB_ICONS_URL = "https://raw.githubusercontent.com/nerazshakya/notify-msteams/main/icons/"
local_timezone = datetime.datetime.now().astimezone().tzinfo

# Format time for display
current_time = datetime.datetime.now(local_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

# Status-based icons mapping
STATUS_ICONS = {
    "Success": "success.png",
    "Failure": "failure.png",
    "Skipped": "skipped.png",
    "Cancelled": "cancelled.png",
    "Unknown": "unknown.png",
    "Person": "github.png"
}

def send_teams_notification():
    """Send an Adaptive Card notification to Microsoft Teams with full details."""

    # Read environment variables from GitHub Actions
    webhook_url = os.getenv('INPUT_WEBHOOK_URL')
    title = os.getenv('INPUT_TITLE', 'GitHub Action Notification')
    status = os.getenv('INPUT_STATUS', 'Unknown')  # Expected: Success, Failure, Skipped, etc.
    commit = os.getenv('GITHUB_SHA', 'Unknown')[:7]  # Short commit hash
    actor = os.getenv('GITHUB_ACTOR', 'Unknown User')
    event = os.getenv('GITHUB_EVENT_NAME', 'Unknown Event')
    repo = os.getenv('GITHUB_REPOSITORY', 'Unknown Repo')
    branch = os.getenv('GITHUB_REF_NAME', 'Unknown Branch')
    commit_message = os.getenv('GITHUB_COMMIT_MESSAGE', 'No commit message')
    run_id = os.getenv('GITHUB_RUN_ID', '')
    files_changed = os.getenv('INPUT_FILES_CHANGED', '')
    github_url = os.getenv('GITHUB_SERVER_URL','https://github.com')
    environ = os.getenv('INPUT_ENVIRON')
    stage = os.getenv('INPUT_STAGE')
    app = os.getenv('INPUT_APP')
    # Ensure required variables are provided
    if not webhook_url:
        raise ValueError("❌ Missing required input: 'INPUT_WEBHOOK_URL'.")

    # Select the correct icon for the status
    icon_url = f"{GITHUB_ICONS_URL}{STATUS_ICONS.get(status, 'unknown.png')}"
    #profile_image_url = f"https://corptb.sharepoint.com/_layouts/15/userphoto.aspx?size=S&username= + {actor} +'@tbdir.net"


    # GitHub links
    repo_url = f"{github_url}/{repo}/tree/{branch}"
    commit_url = f"{github_url}/{repo}/commit/{commit}"
    build_url = f"{github_url}/{repo}/actions/runs/{run_id}"

    # Parse file changes into a formatted list
    files_list = [{"type": "TextBlock", "text": f"• {file.strip()}", "wrap": True} for file in files_changed.split(',') if file.strip()]

    # Construct Adaptive Card JSON
    adaptive_card = {
    "type": "message",
    "attachments": [{
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.6",
            "body": [
                {
                    "type": "Container",
                    "items": [
                
                {
                    "type": "TextBlock",
                    "size": "medium",
                    "weight": "bolder",
                    "text": f"{title}",
                    "spacing": "none"
                },
                {
                    "type": "TextBlock",
                    "size": "small",
                    "weight": "bolder",
                    "text": f"RUN ID #{run_id} (Commit {commit})",
                    "spacing": "none"
                },
                {
                    "type": "TextBlock",
                    "size": "small",
                    "weight": "bolder",
                    "text": f"By @{actor} on {current_time}",
                    "spacing": "none"
                },
                {
                    "type": "FactSet",
                    "separator": True,
                    "spacing": "Padding",
                    "facts": [
                        {"title": "Environment", "value": f"{environ.upper()}", },
                        {"title": "Application", "value": f"{app.upper()}"},
                        {"title": "Stage", "value": f"{stage.upper()}"},
                        {"title": "Event Type", "value": f"{event.capitalize()}"},
                        {"title": "Branch", "value": f"{branch}"},
                        {"title": "Status", "value": f"{status.capitalize()}"},
                        {"title": "Commit Message", "value": f"{commit_message}"}
                    ]
                }
                    ]},
                {
                    "type": "Container",
                    "items": [
                
                {
                    "type": "ActionSet",
                    "actions": [
                        {"type": "Action.OpenUrl","title": "Repository","style": "positive","url": repo_url},
                        {"type": "Action.OpenUrl","title": "Workflow Status","style": "positive","url": build_url},
                        {"type": "Action.OpenUrl","title": "Review Diffs","style": "positive","url": commit_url}
                    ]
                }
                    ]}
            ]
        }
    }]
}
    

    # Remove None values (files list may be empty)
    adaptive_card["attachments"][0]["content"]["body"] = [item for item in adaptive_card["attachments"][0]["content"]["body"] if item]

    # Send request to Teams Webhook
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(adaptive_card))

    if response.status_code == 200:
        print("✅ Notification sent successfully!")
    else:
        print(f"❌ Failed to send notification: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_teams_notification()
