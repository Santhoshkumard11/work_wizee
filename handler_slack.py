import logging
from utils_slack import (
    get_user_id_from_slack,
    get_usergroup_id_by_name,
    get_users_by_usergroup,
    send_message_to_slack,
)


def handle_slack_message(username, message, is_user_group_send):
    """
    Handle sending a message to a Slack user.

    Args:
        username (str): The Slack user name.
        message (str): The message to send.
    """
    try:
        username = username.lower()
        if is_user_group_send:
            logging.info("Sending message to user group.")
            # Assuming usergroup_id is the username for user group send
            user_group_id, created_by_user_id = get_usergroup_id_by_name(username)
            if not user_group_id:
                logging.error("User group not found.")
                return "User group not found."
            # Get users in the user group
            user_ids = get_users_by_usergroup(user_group_id)
            if not user_ids:
                return "No users found in the user group."
            logging.info(f"User IDs in user group {username}: {user_ids}")
            for user_id in user_ids:
                if user_id == created_by_user_id:
                    continue
                send_message_to_slack(user_id, message, "user_client")
            return f"Message sent successfully to user group {username}."
        else:
            slack_user_id = get_user_id_from_slack(username)
            if not slack_user_id:
                return "User not found."
            if not slack_user_id.startswith("U"):
                return "User not found."
            send_message_to_slack(slack_user_id, message)
            return f"Message sent successfully to {username}."
    except Exception as e:
        return f"Error sending message: {e}"
