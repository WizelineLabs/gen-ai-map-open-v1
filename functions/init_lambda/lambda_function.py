import json
import boto3
import os


def handler(event, context):
    queue_url = os.environ["SQS_QUEUE_URL"]

    # Initialize the AWS SQS client
    sqs = boto3.client("sqs")

    values = json.loads(event["body"])

    for value in values["value"]:
        msg = {"value": value[0]}
        r = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(msg))
        print(r)

    return {"statusCode": 200, "body": "Message sent to SQS"}
