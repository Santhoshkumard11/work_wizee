import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_ACCESS_TOKEN = os.environ.get("SLACK_BOT_ACCESS_TOKEN")
SLACK_USER_ACCESS_TOKEN = os.environ.get("SLACK_USER_ACCESS_TOKEN")

# Initialize Slack client once at the top of the file
bot_client = WebClient(token=SLACK_BOT_ACCESS_TOKEN)
user_client = WebClient(token=SLACK_USER_ACCESS_TOKEN)


def send_message_to_slack(user_id: str, message: str, client_to_use="bot_client"):
    """
    Sends a message to a Slack user.

    Args:
        user_id (str): The Slack user ID to send the message to.
        message (str): The message to send.
    """
    client = user_client if client_to_use == "user_client" else bot_client
    try:
        logging.info("Attempting to send message to Slack")
        response = client.chat_postMessage(channel=user_id, text=message)
        if not response["ok"]:
            raise Exception(f"Failed to send message: {response['error']}")
        else:
            logging.info(f"Message sent successfully to {user_id}: {message}")
    except SlackApiError as e:
        raise Exception(f"Slack API error: {e.response['error']}")

def get_user_id_from_slack(user_identifier: str):
    """
    Retrieves a Slack user ID from a username or email.

    Args:
        user_identifier (str): The username or email of the Slack user.

    Returns:
        str: The Slack user ID.
    """
    try:
        if "@" in user_identifier:  # Email lookup
            response = bot_client.users_lookupByEmail(email=user_identifier)
            if response["ok"]:
                return response["user"]["id"]
            else:
                raise Exception(f"Failed to find user by email: {response['error']}")
        else:  # Username lookup
            response = bot_client.users_list()
            if response["ok"]:
                users = response["members"]
                for user in users:
                    if user.get("name") == user_identifier:
                        logging.info(f"User found: {user}")
                        return user.get("id")
                raise Exception(f"User with username {user_identifier} not found.")
            else:
                raise Exception(f"Failed to fetch user list: {response['error']}")
    except SlackApiError as e:
        raise Exception(f"Slack API error: {e.response['error']}")
