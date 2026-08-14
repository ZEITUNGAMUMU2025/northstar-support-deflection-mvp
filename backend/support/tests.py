from django.test import TestCase
from .models import Order


class OrderStatusAPITests(TestCase):

    def setUp(self):
        Order.objects.create(
            order_id=110,
            status="Shipped",
            expected_delivery="2026-06-14",
        )

        Order.objects.create(
            order_id=300,
            status="Processing",
            expected_delivery="2026-06-20",
        )

    def test_shipped_order_returns_correct_status(self):
        response = self.client.get("/api/orders/110")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["order_id"], 110)
        self.assertEqual(response.json()["status"], "Shipped")
        self.assertEqual(
            response.json()["expected_delivery"],
            "2026-06-14",
        )

    def test_processing_order_returns_correct_status(self):
        response = self.client.get("/api/orders/300")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["order_id"], 300)
        self.assertEqual(response.json()["status"], "Processing")
        self.assertEqual(
            response.json()["expected_delivery"],
            "2026-06-20",
        )

    def test_nonexistent_order_returns_not_found(self):
        response = self.client.get("/api/orders/113")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"],
            "Order not found",
        )