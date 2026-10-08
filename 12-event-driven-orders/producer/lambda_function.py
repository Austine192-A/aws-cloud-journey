import json
import os
import uuid
import boto3

sqs = boto3.client("sqs")

QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):
    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        product = body.get("product")
        quantity = body.get("quantity")

        if not product or not quantity:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "product and quantity are required"
                })
            }

        order = {
            "orderId": str(uuid.uuid4()),
            "product": product,
            "quantity": quantity
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(order)
        )

        return {
            "statusCode": 202,
            "body": json.dumps({
                "message": "Order accepted",
                "order": order
            })
        }

    except Exception as error:
        print(f"Error: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to submit order"
            })
        }