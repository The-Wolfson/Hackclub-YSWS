from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
import os

# This Appwrite function will be executed every time your function is triggered
def main(context):
    # You can use the Appwrite SDK to interact with other services
    # For this example, we're using the Users service
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )
    users = Users(client)

    try:
        response = users.list()
        # Log messages and errors to the Appwrite Console
        # These logs won't be seen by your end users
        context.log("Total users: " + str(response["total"]))
    except AppwriteException as err:
        context.error("Could not list users: " + repr(err))

    # The req object contains the request data
    if context.req.path == "/ping":
        # Use res object to respond with text(), json(), or binary()
        # Don't forget to return a response!
        return context.res.text("Pong")

    return context.res.json(
{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "YSWS Programs"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*20* currently active programs found"
			}
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Limited Time"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*<summer.hackclub.com|Summer of Making>*\nBuild stuff. Get stuff. Repeat."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Website"
				},
				"value": "click_me_123"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Ends August 31"
				}
			]
		},
		{
			"type": "divider"
		}
	]
}
    )
