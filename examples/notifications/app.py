import json

from flask import Flask, Response
from flask_schema import Schema, RequestValidationError, ResponseValidationError

app = Flask(__name__)

schema = Schema(cache=True)
schema.init_app(app)


@app.route("/notifications", methods=["POST"])
@schema.check_request("notification_request.schema.json")
@schema.check_response("notification_response.schema.json")
def send_notification():
    # mock the sending of a notification
    app.logger.info("processing request")
    return {"state": "sent", "id": "random-uuid"}


@app.errorhandler(RequestValidationError)
def handle_bad_request(e):
    return Response(json.dumps(e.to_dict()), 400, content_type="application/json")


@app.errorhandler(ResponseValidationError)
def handle_bad_request(e):
    app.logger.exception("response does not match the contract!!! %s", e.to_dict())
    return Response(json.dumps({
        "erorr": "There was an issue while processing the request. Please try again later.",
        "code": "server_error",
    }), 500, content_type="application/json")


if __name__ == "__main__":
    app.run(debug=True)
