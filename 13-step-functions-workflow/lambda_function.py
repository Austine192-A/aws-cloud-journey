import json


def lambda_handler(event, context):
    print(f"Received order: {json.dumps(event)}")

    order_id = event.get("orderId")
    product = event.get("product")
    quantity = event.get("quantity")

    if not order_id or not product:
        raise ValueError("orderId and product are required")

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        raise ValueError("quantity must be a positive integer")

    result = {
        "orderId": order_id,
        "product": product,
        "quantity": quantity,
        "status": "PROCESSED",
        "message": "Order processed successfully"
    }

    print(f"Processing result: {json.dumps(result)}")

    return result
