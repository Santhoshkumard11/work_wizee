import logging

from utils_jira import create_jira_ticket, get_user_details


def handle_create_jira_ticket(
    summary: str,
    description: str,
    assignee: str,
    story_points: int = None,
    issue_type: str = "Task",
    priority: str = "Medium",
    project_key: str = "WOWZEE",
):
    """
    Handles the creation of a JIRA ticket.

    Args:
        project_key (str): The key of the JIRA project.
        summary (str): The summary of the ticket.
        description (str): The description of the ticket.
        assignee (str): The username of the assignee.
        story_points (int, optional): The story points to set.
        sprint_id (int, optional): The sprint ID to set.
        priority (str, optional): The priority to set.

    Returns:
        str: The key of the created ticket.
    """
    try:
        logging.info(
            f"Creating JIRA ticket with summary: {summary}, description: {description}, assignee: {assignee}, story points: {story_points}, issue type: {issue_type}, priority: {priority}"
        )

        user_id = get_user_details(assignee)

        ticket_key, message = create_jira_ticket(
            project_key,
            summary,
            description,
            user_id,
            story_points,
            issue_type,
            priority,
        )

        logging.info(f"JIRA ticket created successfully: {ticket_key}")
        if not ticket_key:
            logging.error("Failed to create JIRA ticket.")
            return message

        return ticket_key
    except Exception as e:
        logging.error(f"Error creating JIRA ticket: {e}")
        return message
