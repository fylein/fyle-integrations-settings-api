import json
import os
import sys
import hmac
import hashlib
import json
import requests
from rest_framework import status


# Create booking against the booker
# Make sure the profile name `Nilesh Pant` is mapped to booker
# and employee `nilesh.p@fyle.in` exists for the org id

def run_test(org_id):

    # Your existing test code here
    payload = {
        "serial_number": "INV-04-00443",
        "profile_id": "b2cca47d-c3bc-4b09-8f86-358a83cae842",
        "profile_name": "Fyle",
        "billing_information": {
            "legal_name": "Fyle",
            "vat_number": None,
            "address_line_1": "B-48 GM Complex",
            "address_line_2": "",
            "city": "Barcelona",
            "postal_code": "480551",
            "country_name": "Spain"
        },
        "mode": "us-reseller",
        "status": "paid",
        "issuing_date": "2024-03-13",
        "billing_period": "instant",
        "from_date": "2024-03-13",
        "to_date": "2024-03-13",
        "due_date": "2024-03-13",
        "currency": "USD",
        "total": "156.34",
        "taxes_summary": [
            {
                "tax_regime": "US-G-VAT-R-0",
                "subtotal": "156.34",
                "tax_percentage": "0.00",
                "tax_amount": "0.00",
                "total": "156.34"
            }
        ],
        "reference": "Trip #10223",
        "travelperk_bank_account": None,
        "pdf": 'https://fyle-storage-prod-2.s3.amazonaws.com/2021-09-29/orwR4RVk6PUr/receipts/fiQK2ap6m3lA.receipt.pdf?response-content-disposition=attachment%3B%20filename%3Dreceipt.pdf&response-content-type=application%2Fpdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240327T101149Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604800&X-Amz-Credential=AKIA54Z3LIXTXIFJ2EXF%2F20240327%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e1e9da9bb64c2aeb52cbb7e2ef817c776f39412f9f5c9055bb144ca65a1d2232',
        "lines": [
            {
                "id": "57b01f5c-62be-43f6-a475-1a41e616c7c5",
                "expense_date": "2024-03-13",
                "description": "PRO for Trip 10223",
                "quantity": 1,
                "unit_price": "4.55",
                "non_taxable_unit_price": "0",
                "tax_percentage": "0.00",
                "tax_amount": "0.00",
                "tax_regime": "US-G-VAT-R-0",
                "total_amount": "4.55",
                "metadata": {
                    "trip_id": 10223,
                    "trip_name": "Nilesh Spain Trip",
                    "service": "pro_v2",
                    "travelers": [
                        {
                            "name": "Ashwin T",
                            "email": "ashwin.t+travelperk@fyle.in",
                            "external_id": None
                        }
                    ],
                    "booker": {
                        "name": "Nilesh Pant",
                        "email": "nilesh.p@fyle.in",
                        "external_id": None
                    },
                    "start_date": None,
                    "end_date": None,
                    "cost_center": "",
                    "labels": [],
                    "vendor": None,
                    "out_of_policy": "",
                    "approvers": [],
                    "service_location": None,
                    "include_breakfast": None,
                    "credit_card_last_4_digits": "1111"
                }
            },
            {
                "id": "8d30ff5f-b55d-4bea-aa51-9368e0796de3",
                "expense_date": "2024-03-13",
                "description": "CAR for Trip ID 10223",
                "quantity": 1,
                "unit_price": "151.79",
                "non_taxable_unit_price": "0",
                "tax_percentage": "0.00",
                "tax_amount": "0.00",
                "tax_regime": "US-G-VAT-R-0",
                "total_amount": "151.79",
                "metadata": {
                    "trip_id": 10223,
                    "trip_name": "Nilesh Spain Trip",
                    "service": "car",
                    "travelers": [
                        {
                            "name": "Ashwin T",
                            "email": "ashwin.t+travelperk@fyle.in",
                            "external_id": None
                        }
                    ],
                    "booker": {
                        "name": "Nilesh Pant",
                        "email": "nilesh.p@fyle.in",
                        "external_id": None
                    },
                    "start_date": "2029-04-17",
                    "end_date": "2029-04-19",
                    "cost_center": "",
                    "labels": [],
                    "vendor": {
                        "code": "SX",
                        "name": "SIXT"
                    },
                    "out_of_policy": True,
                    "approvers": [],
                    "service_location": {
                        "pick_up_location": {
                            "city": "BARCELONA",
                            "country": "Spain",
                            "country_code": "ES",
                            "latitude": "41.392180000",
                            "longitude": "2.162290000"
                        }
                    },
                    "include_breakfast": None,
                    "credit_card_last_4_digits": "1111"
                }
            }
        ]
    }

    api_url = os.environ.get('API_URL')
    url = '{}/orgs/{}/travelperk/travelperk_webhook/'.format(api_url, org_id)

    secret = os.environ.get('TKWEBHOOKS_SECRET')
    signature = hmac.new(secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()

    headers = {
        'tk-webhook-hmac-sha256': signature
    }

    # Send a POST request with valid signature
    response = requests.request("POST", url, headers=headers, data=payload)
    # Assert the response status code and content
    if response.status_code == status.HTTP_200_OK:
        print("Success")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    # Check if an org_id argument is provided
    if len(sys.argv) < 2:
        print("Please provide the organization ID as a command-line argument.")
        sys.exit(1)

    org_id = int(sys.argv[1])
    run_test(org_id)
