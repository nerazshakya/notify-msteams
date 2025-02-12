import main

if __name__ == "__main__":
    try:
        main.send_teams_notification()
    except Exception as e:
        print(f"❌ Error: {e}")