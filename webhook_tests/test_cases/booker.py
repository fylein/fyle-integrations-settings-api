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
        'serial_number': 'INV-04-00441',
        'profile_id': 'a72eccb0-85da-4ca3-ac8b-59242889eff8',
        'profile_name': 'Nilesh Pant',
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
        'issuing_date': '2024-03-13',
        'billing_period': 'instant',
        'from_date': '2024-03-13',
        'to_date': '2024-03-13',
        'due_date': '2024-03-13',
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
        'pdf': 'https://tk-sandbox-backend-data.s3.amazonaws.com/invoices/2067/INV-04-00441.pdf?AWSAccessKeyId=ASIA5MFYTLYHYTL4CSYX&Signature=VbhXde%2FCN5rq%2B5Yj3V850bSxQcY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFAaCWV1LXdlc3QtMSJHMEUCIQDsjSjJyvm3irybBW7Dx1z2I02u8U5so8IgGsh1mZtsAgIgRd7PI1AtT2n6ggic3Vda9GCWh9FGbVzz%2BYiaDAxxXuoq5QMIWRABGgw5MTk1MTAxNDY1NzUiDLu8Jet4SjAOUlB96CrCA6uta149cgfzi64PMSZeu1OJWXTuPZbTeps6udD5v7zhTNEHeSS0X2MrQOPGSKFBHZsz0wGo3%2FncYVa%2FAT806ezEJIvonnysWJhiSPA0pEqn991qOySIDJLpvRqJUqaNkQwaLeY%2BIzj0JIgfrZQazGvbMrppKom2p4OAetVoeRTjHU8BaJZDUlFFw1PDHC2ds1gC1Gfp8jy5ooyEszRDKVbYtdTXO3aoHTW0k378ZNoOHQD4y4N7jcbCakVFTFtzr14nJ8rabQgZ20iLfanmzyl%2Fm8FmajH%2FFSgc2Edwi8DZGmTCB4Yg2iu0tCKyOCIa%2ByKqHwOsovScD6ELVtwZPP4gHE%2BLwYsKt3LZPddwqD2uYLB3Ibt%2B93OnnjaamI%2F5AhH96CBf0vSdgACGkG2ddBfdzyf%2Fvyxlk7iRG6MKB8of6vx2M%2BDa03EEF%2FPQGx43zYHVN0ZpxfOApDtbZICCuw3H4ZacOBOhWSvJ9mxsvSQ17bvK%2BPZXkCeASBgplRJC%2FyMlnO3vfCXMTWhj47HEBFa2naB0lpyMwAR6AfGSKjrPDvffbFAJxXM1HT1L5LsjieTU7cX0wt45H5fkr6Bgicr8dDD5tcWvBjqlASxNGzFgpg5nJtBDFr9zt4gVV8fLJtLd3fRAF0tOwVljI%2BfYNqQYw5Ez%2FQfH6plbFB130MKJTRS4eIFlzhsJp1a1owqGWVE5UvAueEMvKBgeyPnNi7uN5M8Yyu5iOn3NhQuVIIOnA01pgdvfASzQatrije2CDXrdKYJGA9qVc%2BjIdHuUELk7D7WGpCL5oZrDAeGmHwdn4eEVsZKn5iuxMQCoNXUSRQ%3D%3D&Expires=1710321334',
        'lines': [
            {
                'id': '54b4f3c2-11a4-4cb5-a725-1e1346d54def',
                'expense_date': '2024-03-13',
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
                'expense_date': '2024-03-13',
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
    url = '{}/orgs/{0}/travelperk/travelperk_webhook/'.format(api_url, org_id)

    signature = os.environ.get('TEST_SIGNATURE1')

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
