from django.http import JsonResponse
from .models import Order
from datetime import date
from django.http import JsonResponse
from .models import Order
from .return_policies import RETURN_POLICIES

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



def get_return_policy(request, category):
    category = category.lower()

    if category not in RETURN_POLICIES:
        return JsonResponse(
            {
                "error": "Invalid category",
                "message": "Please select clothing, electronics, or furniture."
            },
            status=400
        )

    policy = RETURN_POLICIES[category]

    response = {
        "category": category,
        "return_window_days": policy["return_window_days"],
    }

    if "conditions" in policy:
        response["conditions"] = policy["conditions"]

    if "message" in policy:
        response["message"] = policy["message"]

    return JsonResponse(response)



def get_return_categories(request):
    return JsonResponse(
        {
            "error": "Category required",
            "message": "Please confirm the category of goods you wish to return.",
            "categories": list(RETURN_POLICIES.keys()),
        },
        status=400
    )


def get_return_status(request):
    return JsonResponse({
        "message": (
            "Returns are processed within 4-7 working days "
            "after we receive and inspect the returned item."
        )
    })

def check_return_eligibility(request, category):
    category = category.lower()

    if category not in RETURN_POLICIES:
        return JsonResponse(
            {
                "error": "Invalid category",
                "message": "Please select clothing, electronics, or furniture."
            },
            status=400
        )

    purchase_date_string = request.GET.get("purchase_date")

    if not purchase_date_string:
        return JsonResponse(
            {
                "error": "Purchase date required",
                "message": "Please provide the purchase date in YYYY-MM-DD format."
            },
            status=400
        )

    try:
        purchase_date = date.fromisoformat(purchase_date_string)
    except ValueError:
        return JsonResponse(
            {
                "error": "Invalid purchase date",
                "message": "Please provide the purchase date in YYYY-MM-DD format."
            },
            status=400
        )

    days_since_purchase = (date.today() - purchase_date).days
    return_window = RETURN_POLICIES[category]["return_window_days"]

    if days_since_purchase < 0:
        return JsonResponse(
            {
                "error": "Invalid purchase date",
                "message": "Purchase date cannot be in the future."
            },
            status=400
        )

    if days_since_purchase <= return_window:
        return JsonResponse({
            "category": category,
            "eligible": True,
            "days_since_purchase": days_since_purchase,
            "return_window_days": return_window,
        })

    return JsonResponse({
        "category": category,
        "eligible": False,
        "days_since_purchase": days_since_purchase,
        "return_window_days": return_window,
        "message": (
            "Dear customer, your return window has expired. "
            "Please contact customer support for assistance."
        ),
    })

