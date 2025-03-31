from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import user_settings
# Skapa en klient för att interagera med Slack API
client = WebClient(token=data.SLACK_BOT_TOKEN )

def send_slack_message(message):
    try:
        client.chat_postMessage(
            channel=user_settings.SLACK_ACCOUNT,  # Du kan använda ditt eget Slack-användarnamn
            text=message
        )
        print("✅ Meddelande skickat till Slack-botens egen vy!")
    except SlackApiError as e:
        print(f"❌ Slack API-fel: {e.response['error']}")
