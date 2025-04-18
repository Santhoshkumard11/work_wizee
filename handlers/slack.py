from utils.slack import get_user_id_from_slack, send_message_to_slack


def handle_slack_message(username, message):
    """
    Handle sending a message to a Slack user.

    Args:
        username (str): The Slack user name.
        message (str): The message to send.
    """
    try:
        slack_user_id = get_user_id_from_slack(username)
        if not slack_user_id:
            return "User not found."
        if not slack_user_id.startswith("U"):
            return "User not found."
        send_message_to_slack(slack_user_id, message)
        return f"Message sent successfully to {username}."
    except Exception as e:
        return f"Error sending message: {e}"
