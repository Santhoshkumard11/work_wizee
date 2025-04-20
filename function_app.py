import azure.functions as func
import logging
import urllib.parse

from handler_jira import (
    handle_create_jira_ticket,
    handle_get_latest_comments,
    handle_jira_add_comment,
)
from handler_slack import handle_slack_create_channel_for_users, handle_slack_message

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)


@app.route(route="jira_add_comment", methods=["POST"])
def jira_add_comment(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira add comment HTTP trigger function processed a request.")
    response_message = "Jira comment added successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        ticket_key = params.get("ticket_key", [""])[0]
        comment = params.get("comment", [""])[0]

        logging.info(f"Ticket Key - {ticket_key} - Comment - {comment}")

        response_message = handle_jira_add_comment(ticket_key, comment)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to add comment to Jira ticket - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="jira_get_latest_comments", methods=["POST"])
def jira_get_latest_comments(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira get latest comments HTTP trigger function processed a request.")
    response_message = "Jira latest comments - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        ticket_key = params.get("ticket_key", [""])[0]

        response_message = handle_get_latest_comments(ticket_key)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = (
            f"Error while trying to get latest comments from Jira ticket - {e}"
        )

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="jira_create_ticket", methods=["POST"])
def jira_create_ticket(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira create ticket HTTP trigger function processed a request.")
    response_message = "Jira ticket created successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        summary = params.get("summary", [""])[0]
        description = params.get("description", [""])[0]
        assignee = params.get("assignee", [""])[0]
        # default story points is 3
        story_points = params.get("story_points", ["3"])[0]
        issue_type = params.get(
            "issue_type",
            ["Task"],
        )[0]
        priority = params.get("priority", [""])[0]

        jira_ticket = handle_create_jira_ticket(
            summary, description, assignee, story_points, issue_type, priority
        )

        response_message = (
            response_message
            + f"ticket Key - {jira_ticket} and ticket URL is https://sandyinspires.atlassian.net/browse/{jira_ticket}."
        )

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to create Jira ticket - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="slack_create_channel_for_users", methods=["POST"])
def slack_create_channel_for_users(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        "Slack create channel for users HTTP trigger function processed a request."
    )
    response_message = "Slack channel created successfully for "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        list_of_users = params.get("list_of_users", [""])[0]
        individual_user_message = params.get("individual_user_message", [""])[0]
        channel_name = params.get("channel_name", [""])[0]
        # default channel visibility is private
        channel_visibility = params.get("channel_visibility", ["private"])[0]
        channel_first_message = params.get(
            "channel_first_message",
            ["Create this channel to discussion about the ongoing issue"],
        )[0]

        response_message = handle_slack_create_channel_for_users(
            list_of_users,
            individual_user_message,
            channel_name,
            channel_visibility,
            channel_first_message,
        )

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = "Error processing request."

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="slack_send_message", methods=["POST"])
def slack_send_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Slack Send Message HTTP trigger function processed a request.")

    response_message = "Slack message sent successfully to "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        username = params.get("username", [""])[0]
        message_body = params.get("slack_message", [""])[0]
        is_user_group_send = (
            params.get("is_user_group_send", ["false"])[0].lower() == "true"
        )

        logging.info(
            f"Username - {username} - Message - {message_body} - is_user_group_send - {is_user_group_send}"
        )

        response_handle_slack_message = handle_slack_message(
            username, message_body, is_user_group_send
        )

        response_message = response_handle_slack_message
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = "Error processing request."

    return func.HttpResponse(
        response_message,
        status_code=200,
    )
