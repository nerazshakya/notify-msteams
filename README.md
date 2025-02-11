# notify-msteams
# Send Notification to Teams Channel

name: Notify Teams
on: 
  push:
    branches:
      - main

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send Notification
        uses: nerazshakya/notify-msteams@main
        with:
          webhook_url: ${{ secrets.TEAMS_WEBHOOK_URL }}
          title: "New Deployment"
          message: "A new change has been pushed to main."
          status: "Success"
