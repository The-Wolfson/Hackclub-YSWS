def help(context):
    context.res.json({
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Hackclub Events"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*<@U094ELS98UC>*"
				},
				{
					"type": "plain_text",
					"text": "A Slack app to keep you up to date with Hackclub's events, hackathons, and YSWS programs."
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Usage: /ysws"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*filter:*\n• all\n• active _(default)_\n• draft\n• ended"
				},
				{
					"type": "mrkdwn",
					"text": "*sort:*\n• alphabetical\n• category\n• date _(default)_\n• status"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "▶️ `/ysws filter:ended sort:alphabetical` – List of ended YSWS programs sorted in alphabetical order."
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Usage: /events"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*filter:*\n• all\n• ended\n• upcoming _(default)_"
				},
				{
					"type": "mrkdwn",
					"text": "*sort:*\n• alphabetical\n• date _(default)_"
				},
				{
					"type": "mrkdwn",
					"text": "*type:*\n• all _(default)_\n• event\n• ama"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "▶️ `/events filter:all sort:alphabetical type:ama` – List of all Hackclub AMAs sorted in alphabetical order."
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Usage: /hackathons"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*filter:*\n• all\n• active _(default)_\n• upcoming\n• ended"
				},
				{
					"type": "mrkdwn",
					"text": "*sort:*\n• alphabetical\n• modality\n• date _(default)_"
				},
				{
					"type": "mrkdwn",
					"text": "*modality:*\n• all _(default)_\n• online\n• in-person\n• hybrid"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "▶️ `/hackathons filter:upcoming sort:alphabetical modality:online` – List of upcoming online hackathons sorted in alphabetical order."
				}
			]
		}
	]
})