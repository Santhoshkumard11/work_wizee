import json
import azure.functions as func
import logging
import urllib.parse

from handler_slack import handle_slack_message

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)


@app.route(route="slack_search_userid", methods=["POST"])
def slack_search_userid(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Slack Search User ID HTTP trigger function processed a request.")
    try:
        req_body = req.get_json()
        logging.info(f"body - {req_body}")
    except ValueError:
        pass

    return_response = json.dumps({"user_id": "U123456"})

    return func.HttpResponse(
        return_response,
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

        logging.info(f"Username - {username} - Message - {message_body}")

        response_handle_slack_message = handle_slack_message(username, message_body)

        response_message = response_handle_slack_message
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = "Error processing request."

    return func.HttpResponse(
        response_message,
        status_code=200,
    )
