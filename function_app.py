import json
import azure.functions as func
import logging

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
    try:
        req_body = req.get_json()
        logging.info(f"body - {req_body}")
    except ValueError:
        pass

    return func.HttpResponse(
        "Slack message sent successfully.",
        status_code=200,
    )
