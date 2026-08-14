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

    def test_missing_order_id_returns_validation_error(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
        response.json()["error"],
        "Order number required",
    )

    def test_invalid_order_id_format_returns_validation_error(self):
        response = self.client.get("/api/orders/300*")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
        response.json()["error"],
        "Invalid order number",
    )    
        


class ReturnAPITests(TestCase):

    def test_clothing_return_policy(self):
        response = self.client.get("/api/returns/clothing")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "clothing")
        self.assertEqual(response.json()["return_window_days"], 10)
        self.assertEqual(
            response.json()["conditions"],
            "unworn with original tag intact",
        )

    def test_electronics_return_policy(self):
        response = self.client.get("/api/returns/electronics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "electronics")
        self.assertEqual(response.json()["return_window_days"], 20)
        self.assertIn(
            "return portal",
            response.json()["message"],
        )

    def test_furniture_return_policy(self):
        response = self.client.get("/api/returns/furniture")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "furniture")
        self.assertEqual(response.json()["return_window_days"], 7)
        self.assertEqual(
            response.json()["conditions"],
            "original packaging",
        )

    def test_missing_return_category(self):
        response = self.client.get("/api/returns/")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Category required",
        )

    def test_expired_return_window(self):
        response = self.client.get(
            "/api/returns/clothing/check"
            "?purchase_date=2026-07-01"
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["eligible"])
        self.assertIn(
            "return window has expired",
            response.json()["message"],
        )

    def test_return_status(self):
        response = self.client.get("/api/returns/status")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "4-7 working days",
            response.json()["message"],
        )    


    def test_eligible_return(self):
        response = self.client.get(
            "/api/returns/clothing/check"
            "?purchase_date=2026-08-10"
    )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["eligible"])        


    def test_invalid_purchase_date(self):
        response = self.client.get(
            "/api/returns/clothing/check"
            "?purchase_date=banana"
    )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Invalid purchase date",
    )  


    def test_future_purchase_date(self):
        response = self.client.get(
            "/api/returns/clothing/check"
            "?purchase_date=2099-01-01"
    )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Invalid purchase date",
    )      