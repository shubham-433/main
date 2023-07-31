from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_invoice(self):
        data = {
            "date": "2023-07-31",
            "invoice_no": "INV-001",
            "customer_name": "John Doe",
            "details": [
                {
                    "description": "Item 1",
                    "quantity": 2,
                    "unit_price": "10.00",
                    "price": "20.00"
                },
                {
                    "description": "Item 2",
                    "quantity": 1,
                    "unit_price": "15.00",
                    "price": "15.00"
                }
            ]
        }

        response = self.client.post('http://127.0.0.1:8000/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        

    def test_get_invoice_list(self):
        # Create test data
        invoice1 = Invoice.objects.create(
            date="2023-07-31",
            invoice_no="INV-001",
            customer_name="John Doe"
        )
        invoice2 = Invoice.objects.create(
            date="2023-07-30",
            invoice_no="INV-002",
            customer_name="Jane Smith"
        )

        response = self.client.get('http://127.0.0.1:8000/invoices/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check if the response data matches the test data
        self.assertEqual(response.data[0]['id'], invoice1.id)
        self.assertEqual(response.data[0]['date'], "2023-07-31")
        self.assertEqual(response.data[0]['invoice_no'], "INV-001")
        self.assertEqual(response.data[0]['customer_name'], "John Doe")

        self.assertEqual(response.data[1]['id'], invoice2.id)
        self.assertEqual(response.data[1]['date'], "2023-07-30")
        self.assertEqual(response.data[1]['invoice_no'], "INV-002")
        self.assertEqual(response.data[1]['customer_name'], "Jane Smith")
