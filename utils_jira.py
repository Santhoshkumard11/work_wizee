import logging
from jira import JIRA
import os

# Initialize JIRA client
jira_server = os.environ.get("JIRA_SERVER")
jira_token = os.environ.get("JIRA_ACCESS_TOKEN")
jira_email = os.environ.get("JIRA_EMAIL_ADDRESS")
jira_client = JIRA(server=jira_server, basic_auth=(jira_email, jira_token))


def create_jira_ticket(
    project_key: str,
    summary: str,
    description: str,
    user_id: str,
    story_points: str,
    issue_type: str,
    priority: str,
):
    """
    Creates a JIRA ticket and assigns it to a user.

    Args:
        project_key (str): The key of the JIRA project.
        summary (str): The summary of the ticket.
        description (str): The description of the ticket.
        user_id (str): The user_id of the username.

    Returns:
        str: The key of the created ticket.
    """
    story_points = int(story_points) if story_points else 0
    priority = priority.lower().capitalize()
    issue_type = issue_type.lower().capitalize()
    if issue_type not in ["Task", "Bug", "Story"]:
        logging.error(f"Invalid issue type: {issue_type}")
        return None, "Invalid issue type"
    if priority not in ["Highest", "High", "Medium", "Low", "Lowest"]:
        logging.error(f"Invalid priority: {priority}")
        return None, "Invalid priority"
    issue_dict = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
        "assignee": {"accountId": user_id},
        "customfield_10016": story_points,
        "priority": {"name": priority},
    }

    # if it's a bug remove the priority field
    if issue_type == "Bug":
        issue_dict.pop("priority", None)
        logging.info(f"Removing priority field for issue type: {issue_type}")

    logging.info(
        f"Creating JIRA ticket with summary: {summary}, description: {description}"
    )
    logging.info(
        f"Assignee: {user_id}, Story Points: {story_points}, Issue Type: {issue_type}, Priority: {priority}"
    )

    issue = jira_client.create_issue(fields=issue_dict)
    return issue.key, "Ticket created successfully"


def update_jira_ticket(
    ticket_key: str,
    story_points: int = None,
    assignee: str = None,
    sprint_id: int = None,
    priority: str = None,
):
    """
    Updates a JIRA ticket with story points, sprint, assignee, and priority.

    Args:
        ticket_key (str): The key of the JIRA ticket.
        story_points (int, optional): The story points to set.
        sprint_id (int, optional): The sprint ID to set.
        assignee (str, optional): The username of the assignee.
        priority (str, optional): The priority to set.
    """
    fields = {}
    if story_points is not None:
        fields["customfield_10016"] = (
            story_points  # Replace with your JIRA instance's story points field ID
        )
    if sprint_id is not None:
        fields["customfield_10007"] = (
            sprint_id  # Replace with your JIRA instance's sprint field ID
        )
    if assignee is not None:
        fields["assignee"] = {"name": assignee}
    if priority is not None:
        fields["priority"] = {"name": priority}

    jira_client.issue(ticket_key).update(fields=fields)


def comment_on_jira_ticket(ticket_key: str, comment: str):
    """
    Adds a comment to a JIRA ticket.

    Args:
        ticket_key (str): The key of the JIRA ticket.
        comment (str): The comment to add.
    """
    jira_client.add_comment(ticket_key, comment)


def get_latest_comment_from_jira(ticket_key: str):
    """
    Retrieves the latest comment from a JIRA ticket.

    Args:
        ticket_key (str): The key of the JIRA ticket.

    Returns:
        str: The latest comment.
    """
    comments = jira_client.comments(ticket_key)
    if comments:
        return comments[-1].body
    return None


def get_user_details(username: str):
    """
    Retrieves user details from JIRA.

    Args:
        username (str): The username of the user.

    Returns:
        str: The account ID of the user.
    """

    user_details = jira_client.search_users(query=username, maxResults=1)[0]
    if user_details:
        logging.info(f"User details found - {user_details.displayName}")
        return user_details.accountId
    return None
