from django.http import JsonResponse
from .models import Order


def get_order_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)

        return JsonResponse({
            "order_id": order.order_id,
            "status": order.status,
            "expected_delivery": order.expected_delivery,
        })

    except Order.DoesNotExist:
        return JsonResponse(
            {
                "error": "Order not found",
                "message": "Please verify your order number."
            },
            status=404
        )