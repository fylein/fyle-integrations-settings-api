import os
import sys
import requests
from rest_framework import status

# Create booking against the booker
# Make sure the profile name `Nilesh Pant` is mapped to booker
# and employee `nilesh.p@fyle.in` exists for the org id

def run_test(org_id):

    # Your existing test code here
    payload = {
            "serial_number": "INV-04-00442",
            "profile_id": "a72eccb0-85da-4ca3-ac8b-59242889eff8",
            "profile_name": "Nilesh Pant",
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
            "total": "2062.37",
            "taxes_summary": [
                {
                    "tax_regime": "US-G-VAT-R-0",
                    "subtotal": "2062.37",
                    "tax_percentage": "0.00",
                    "tax_amount": "0.00",
                    "total": "2062.37"
                }
            ],
            "reference": "Trip #10221",
            "travelperk_bank_account": None,
            "pdf": "https://tk-sandbox-backend-data.s3.amazonaws.com/invoices/2067/INV-04-00442.pdf?AWSAccessKeyId=ASIA5MFYTLYHZAE5OIYY&Signature=xsVlI9G7fYUfyzBD0VaDVMaHk6U%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFEaCWV1LXdlc3QtMSJHMEUCIBsrPxxN2FlaEmE4S8TK%2FSf9jiu0pxmAbba9la3X5q42AiEAi7GbK7i6vL7bNfgi1Fmtmr7WMIKluKOwUeHC%2BGRsPkIq5QMIWhABGgw5MTk1MTAxNDY1NzUiDKCqZ87uuy0o5qodUSrCAwtN%2BRBmaqvNhWqgJQnIsI4alaLRvCjZAKWlRHD3rWt8kUnYuT6ToT%2B01L0qgt9GkwTd1CGz55cW1uAFNmJK2%2Fa2WS3D1xRhRHlWDcLQK6hilxS3NLyil%2FPbIMYKVaIqO65%2FZUq7hXIQRlQOobgu8Uw6lGTunK1AXxvB21ZjsfFmeXgmvjllYh1FJ6JGvzlKNynA5cC%2FuheeBEtv9ILZ5gpTyXymFShn2NN7VH4R6Lnl4g0u5xvTmwlosRXiylbWCR9d56CFyRjtiA184DUe%2FG4cVtzws0AB9NVeYc9kfaiFveoRuewzCjuOODZ9QozsdbgADL89W5C0%2FFAbI9YXg1H889Ke3wYqmvDQUhf1iN6%2F7cp6c9qr6QoqO57qIgOfoTx9jMbLj110gRxreprcpooWGcJoN49pBw9r64JZntnL%2BVsbWxWulqwgTYrYda5dNqwsrGBrywoL8lvsjJP%2Bo1uMi4w80NyzB8cIpBdLAq4JJ%2BpxKdsdCzPQqkAKF5xsVKrCqKIXygzuIAKbRxDyOcdb0QOextYJmJVhlwOLB8IKMw0wQ4rHWchG%2B65gGTAayuJEWjIEJxcgVCyKLeqyBzRwUDCc28WvBjqlAaS%2BnFYFf82p1AtK2zY96kHTetm%2BaLECXX1Cr7%2BIqAK9qUz0blp0HS%2BQDkQETbi%2FZlkpvNshn%2F8K5eBm1hz%2FP3ldEQ%2FqmtK1fescuWPSnB1xIcVUGVovqZEESyV0h9rx5T6Lamra7WAWsW1BjG4Pc5Ay%2FIbb3ZcTd4BK25st6LD2x2PF9oImTTQF6P4dZ0iJN1lHoE8wMevKdUwvH2KbhJHbPU4G1w%3D%3D&Expires=1710324801",
            "lines": [
                {
                    "id": "a19bb44a-a611-49e5-bdd8-615024023a84",
                    "expense_date": "2024-03-13",
                    "description": "PRO for Trip 10221",
                    "quantity": 1,
                    "unit_price": "30.00",
                    "non_taxable_unit_price": "0",
                    "tax_percentage": "0.00",
                    "tax_amount": "0.00",
                    "tax_regime": "US-G-VAT-R-0",
                    "total_amount": "30.00",
                    "metadata": {
                        "trip_id": 10221,
                        "trip_name": "Stay in Barcelona, Mar 23 - Mar 24",
                        "service": "pro_v2",
                        "travelers": [
                            {
                                "name": "Nilesh Pant",
                                "email": "nilesh.p@fyle.in",
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
                        "credit_card_last_4_digits": "4242"
                    }
                },
                {
                    "id": "c8b818cc-9f39-46e4-92a5-0d153ecf9f83",
                    "expense_date": "2024-03-13",
                    "description": "HOTEL for Trip ID 10221",
                    "quantity": 1,
                    "unit_price": "2032.37",
                    "non_taxable_unit_price": "0",
                    "tax_percentage": "0.00",
                    "tax_amount": "0.00",
                    "tax_regime": "US-G-VAT-R-0",
                    "total_amount": "2032.37",
                    "metadata": {
                        "trip_id": 10221,
                        "trip_name": "Stay in Barcelona, Mar 23 - Mar 24",
                        "service": "hotel",
                        "travelers": [
                            {
                                "name": "Nilesh Pant",
                                "email": "nilesh.p@fyle.in",
                                "external_id": None
                            }
                        ],
                        "booker": {
                            "name": "Nilesh Pant",
                            "email": "nilesh.p@fyle.in",
                            "external_id": None
                        },
                        "start_date": "2024-03-23",
                        "end_date": "2024-03-24",
                        "cost_center": "",
                        "labels": [],
                        "vendor": {
                            "code": None,
                            "name": "Iberostar Paseo de Gracia"
                        },
                        "out_of_policy": True,
                        "approvers": [],
                        "service_location": {
                            "hotel_location": {
                                "city": "Barcelona",
                                "country": "Spain",
                                "country_code": "ES",
                                "latitude": "41.38785",
                                "longitude": "2.16938"
                            }
                        },
                        "include_breakfast": None,
                        "credit_card_last_4_digits": "4242"
                    }
                }
            ]
        }

    api_url = os.environ.get('API_URL')
    url = '{}/orgs/{0}/travelperk/travelperk_webhook/'.format(api_url, org_id)

    signature = os.environ.get('TEST_SIGNATURE3')

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
