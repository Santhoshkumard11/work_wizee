import logging
from utils_slack import (
    add_users_to_channel,
    create_slack_channel,
    get_user_id_from_username,
    get_usergroup_id_by_name,
    get_users_by_usergroup,
    send_message_to_slack,
)


def handle_slack_create_channel_for_users(
    list_of_users,
    message_to_send,
    channel_name,
    channel_visibility,
    channel_first_message,
):
    """
    Handle creating a Slack channel for a list of users.

    Args:
        list_of_users (str): Comma-separated list of Slack user names.
        message_to_send (str): The message to send to the users.
        channel_name (str): The name of the channel to create.
        channel_visibility (str): The visibility of the channel (private or public).
        channel_first_message (str): The first message to send in the channel.
    Returns:
        str: Confirmation message.
    """
    try:
        list_of_users = list_of_users.split(",")
        list_of_users = [user.strip() for user in list_of_users]
        logging.info(f"List of users: {list_of_users}")
        if not list_of_users:
            return "No users provided."

        if not channel_name:
            return "Channel name is required."

        # Create the channel
        channel_id = create_slack_channel(channel_name, channel_visibility)
        if not channel_id:
            return "Failed to create channel."

        logging.info(f"Channel created with ID: {channel_id}")

        list_of_user_ids = []

        for user in list_of_users:
            user_id = get_user_id_from_username(user)
            if not user_id:
                return f"User {user} not found."
            list_of_user_ids.append(user_id)
            send_message_to_slack(user_id, message_to_send, "user_client")

        add_users_to_channel(channel_id, list_of_user_ids)

        # send a message to the channel
        send_message_to_slack(channel_id, channel_first_message)

        return f"Channel '{channel_name}' created successfully with visibility '{channel_visibility}'."
    except Exception as e:
        logging.exception(f"Error creating channel: {e}")
        return f"Error creating channel: {e}"


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
            slack_user_id = get_user_id_from_username(username)
            if not slack_user_id:
                return "User not found."
            if not slack_user_id.startswith("U"):
                return "User not found."
            send_message_to_slack(slack_user_id, message)
            return f"Message sent successfully to {username}."
    except Exception as e:
        return f"Error sending message: {e}"
