import pytest
from unittest.mock import patch, MagicMock
from utils_slack import (
    send_message_to_slack,
    get_user_id_from_username,
    get_users_by_usergroup,
    get_usergroup_id_by_name,
    create_slack_channel,
    add_users_to_channel,
)

@patch("utils_slack.bot_client")
def test_send_message_to_slack(mock_bot_client):
    mock_bot_client.chat_postMessage.return_value = {"ok": True}
    send_message_to_slack("U12345", "Hello, World!")
    mock_bot_client.chat_postMessage.assert_called_once_with(channel="U12345", text="Hello, World!")

@patch("utils_slack.bot_client")
def test_get_user_id_from_username(mock_bot_client):
    mock_bot_client.users_lookupByEmail.return_value = {"ok": True, "user": {"id": "U12345"}}
    user_id = get_user_id_from_username("test@example.com")
    assert user_id == "U12345"

@patch("utils_slack.bot_client")
def test_get_users_by_usergroup(mock_bot_client):
    mock_bot_client.usergroups_users_list.return_value = {"ok": True, "users": ["U12345", "U67890"]}
    users = get_users_by_usergroup("S12345")
    assert users == ["U12345", "U67890"]

@patch("utils_slack.bot_client")
def test_get_usergroup_id_by_name(mock_bot_client):
    mock_bot_client.usergroups_list.return_value = {"ok": True, "usergroups": [{"name": "TestGroup", "id": "S12345"}]}
    usergroup_id, _ = get_usergroup_id_by_name("TestGroup")
    assert usergroup_id == "S12345"

@patch("utils_slack.bot_client")
def test_create_slack_channel(mock_bot_client):
    mock_bot_client.conversations_create.return_value = {"ok": True, "channel": {"id": "C12345"}}
    channel_id = create_slack_channel("test-channel", "private")
    assert channel_id == "C12345"

@patch("utils_slack.bot_client")
def test_add_users_to_channel(mock_bot_client):
    mock_bot_client.conversations_invite.return_value = {"ok": True}
    add_users_to_channel("C12345", ["U12345", "U67890"])
    mock_bot_client.conversations_invite.assert_called_once_with(channel="C12345", users="U12345,U67890")