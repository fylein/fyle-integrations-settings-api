import os
import sys
import requests
import hmac
import hashlib
import json
from rest_framework import status


# Create booking against the booker
# Make sure the profile name `Nilesh Pant` is mapped to booker
# and employee `nilesh.p@fyle.in` exists for the org id

def run_test(org_id):

    # Your existing test code here
    payload = {
        'serial_number': 'INV-04-00441',
        'profile_id': 'a72eccb0-85da-4ca3-ac8b-59242889eff8',
        'profile_name': 'Fyle',
        'billing_information': {
            'legal_name': 'Fyle',
            'vat_number': None,
            'address_line_1': 'B-48 GM Complex',
            'address_line_2': '',
            'city': 'Barcelona',
            'postal_code': '480551',
            'country_name': 'Spain'
        },
        'mode': 'us-reseller',
        'status': 'paid',
        'issuing_date': '2024-03-26',
        'billing_period': 'instant',
        'from_date': '2024-03-26',
        'to_date': '2024-03-26',
        'due_date': '2024-03-26',
        'currency': 'USD',
        'total': '124.25',
        'taxes_summary': [
            {
                'tax_regime': 'US-G-VAT-R-0',
                'subtotal': '124.25',
                'tax_percentage': '0.00',
                'tax_amount': '0.00',
                'total': '124.25'
            }
        ],
        'reference': 'Trip #10220',
        'travelperk_bank_account': None,
        'pdf': 'https://fyle-storage-prod-2.s3.amazonaws.com/2021-09-29/orwR4RVk6PUr/receipts/fiQK2ap6m3lA.receipt.pdf?response-content-disposition=attachment%3B%20filename%3Dreceipt.pdf&response-content-type=application%2Fpdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240327T101149Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604800&X-Amz-Credential=AKIA54Z3LIXTXIFJ2EXF%2F20240327%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e1e9da9bb64c2aeb52cbb7e2ef817c776f39412f9f5c9055bb144ca65a1d2232',
        'lines': [
            {
                'id': '54b4f3c2-11a4-4cb5-a725-1e1346d54def',
                'expense_date': '2024-03-26',
                'description': 'PRO for Trip 10220',
                'quantity': 1,
                'unit_price': '3.62',
                'non_taxable_unit_price': '0',
                'tax_percentage': '0.00',
                'tax_amount': '0.00',
                'tax_regime': 'US-G-VAT-R-0',
                'total_amount': '3.62',
                'metadata': {
                    'trip_id': 10220,
                    'trip_name': 'Flight to West Lisaville, May 18 - May 19',
                    'service': 'pro_v2',
                    'travelers': [
                        {
                            'name': 'Kamalini Yuvaraj',
                            'email': 'kamalini.y@fyle.in',
                            'external_id': None
                        }
                    ],
                    'booker': {
                        'name': 'Nilesh Pant',
                        'email': 'nilesh.p@fyle.in',
                        'external_id': None
                    },
                    'start_date': None,
                    'end_date': None,
                    'cost_center': '',
                    'labels': [],
                    'vendor': None,
                    'out_of_policy': '',
                    'approvers': [],
                    'service_location': None,
                    'include_breakfast': None,
                    'credit_card_last_4_digits': '4242'
                }
            },
            {
                'id': 'ee56fc53-4a4f-4a19-b3b0-fb60a8c94659',
                'expense_date': '2024-03-26',
                'description': 'FLIGHT for Trip ID 10220',
                'quantity': 1,
                'unit_price': '120.63',
                'non_taxable_unit_price': '0',
                'tax_percentage': '0.00',
                'tax_amount': '0.00',
                'tax_regime': 'US-G-VAT-R-0',
                'total_amount': '120.63',
                'metadata': {
                    'trip_id': 10220,
                    'trip_name': 'Flight to West Lisaville, May 18 - May 19',
                    'service': 'flight',
                    'travelers': [
                        {
                            'name': 'Kamalini Yuvaraj',
                            'email': 'kamalini.y@fyle.in',
                            'external_id': None
                        }
                    ],
                    'booker': {
                        'name': 'Nilesh Pant',
                        'email': 'nilesh.p@fyle.in',
                        'external_id': None
                    },
                    'start_date': '2024-05-19',
                    'end_date': '2030-04-17',
                    'cost_center': '',
                    'labels': [],
                    'vendor': {
                        'code': 'VY',
                        'name': 'Vueling'
                    },
                    'out_of_policy': True,
                    'approvers': [],
                    'service_location': {
                        'origin': {
                            'name': 'Salasstad Airport',
                            'code': 'MAD',
                            'city': 'West Lisaville',
                            'country': 'Trinidad and Tobago',
                            'country_code': 'VE',
                            'latitude': '15.4886261',
                            'longitude': '131.0075138'
                        },
                        'destination': {
                            'name': 'North Tara Airport',
                            'code': 'BCN',
                            'city': 'Oliviaport',
                            'country': 'Bulgaria',
                            'country_code': 'BY',
                            'latitude': '76.5021054',
                            'longitude': '42.3743066'
                        }
                    },
                    'include_breakfast': None,
                    'credit_card_last_4_digits': '4242'
                }
            }
        ]
    }

    api_url = os.environ.get('API_URL')
    url = '{}/orgs/{}/travelperk/travelperk_webhook/'.format(api_url, org_id)

    secret = os.environ.get('TKWEBHOOKS_SECRET')
    signature = hmac.new(secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()

    headers = {
        'tk-webhook-hmac-sha256': signature,
        'Content-Type': 'application/json'
    }

    # Send a POST request with valid signature
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
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
