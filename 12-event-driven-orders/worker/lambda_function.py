import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    for record in event["Records"]:
        order = json.loads(record["body"])

        table.put_item(
            Item={
                "orderId": order["orderId"],
                "product": order["product"],
                "quantity": order["quantity"],
                "status": "PROCESSED"
            }
        )

        print(f"Processed order: {order['orderId']}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Orders processed successfully"
        })
    }