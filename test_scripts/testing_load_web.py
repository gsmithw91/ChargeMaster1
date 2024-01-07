import requests
import csv
import os
from time import time, strftime
from statistics import mean
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# Create test_results directory if it doesn't exist
os.makedirs('test_results', exist_ok=True)

endpoints = [
    'https://smithtech.io/api/systems',
    'https://smithtech.io/api/systems/4',  # Example: Use an actual system_id that exists in your database.
    'https://smithtech.io/api/locations',
    'https://smithtech.io/api/locations/1',  # Example: Use an actual system_id that exists in your database.
    'https://smithtech.io/api/charges/system/4/location/27',  # Example: Use actual system_id and location_id values.
    'https://smithtech.io/react/eligibility/carriers',
    'https://smithtech.io/react/eligibility/carriers/1',
    'https://smithtech.io/react/eligibility/carriers/2',
    'https://smithtech.io/react/eligibility/carriers/3',
    'https://smithtech.io/react/eligibility/carriers/4',
    'https://smithtech.io/react/eligibility/carriers/5',
    'https://smithtech.io/react/eligibility/carriers/6',
    'https://smithtech.io/react/eligibility/carriers/7',
    'https://smithtech.io/react/eligibility/insurances',
    'https://smithtech.io/react/eligibility/insurances/1',
    'https://smithtech.io/react/eligibility/insurances/2',
    'https://smithtech.io/react/eligibility/insurances/3',
    'https://smithtech.io/react/eligibility/insurances/4',
    'https://smithtech.io/react/eligibility/insurances/5',
    'https://smithtech.io/react/eligibility/insurances/6',
    'https://smithtech.io/react/eligibility/insurances/7',
    'https://smithtech.io/react/eligibility/insurances/8',
    'https://smithtech.io/react/eligibility/insurances/9',
    'https://smithtech.io/react/eligibility/insurances/10',
    'https://smithtech.io/react/eligibility/insurance-types',
    'https://smithtech.io/react/eligibility/insurance-types/1',
    'https://smithtech.io/react/eligibility/insurance-types/2',
    'https://smithtech.io/react/eligibility/insurance-types/3',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/1',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/2',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/3',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/4',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/5',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/6',
    'https://smithtech.io/react/eligibility/insurance-plans/1',
    'https://smithtech.io/react/eligibility/insurance-plans/2',
    'https://smithtech.io/react/eligibility/insurance-plans/3',
    'https://smithtech.io/react/eligibility/insurance-plans/4',
    'https://smithtech.io/react/eligibility/insurance-plans/5',
    'https://smithtech.io/react/eligibility/insurance-plans/6',
    'https://smithtech.io/react/eligibility/records/system/1',
    'https://smithtech.io/react/eligibility/records/system/2',
    'https://smithtech.io/react/eligibility/records/system/3',
    'https://smithtech.io/react/eligibility/records/system/3',
    'https://smithtech.io/react/eligibility/records/system/4',
    'https://smithtech.io/react/eligibility/records/system/4/location/17',
    'https://smithtech.io/react/eligibility/records/system/4/location/18',
    'https://smithtech.io/react/eligibility/records/system/4/location/19',
    'https://smithtech.io/react/eligibility/records/system/4/location/20',
    'https://smithtech.io/react/eligibility/network-info/1',
    'https://smithtech.io/react/eligibility/network-info/2',
    'https://smithtech.io/react/eligibility/network-info/3',
    'https://smithtech.io/react/eligibility/network-info/4',
    'https://smithtech.io/react/eligibility/network-info/5',
    'https://smithtech.io/react/eligibility/network-info/6',
    'https://smithtech.io/db_admin/tables',
    'https://smithtech.io/db_admin/columns/HospitalSystem',
    'https://smithtech.io/db_admin/columns/HospitalLocation',
    'https://smithtech.io/db_admin/columns/Charges_Northwestern',
    'https://smithtech.io/db_admin/columns/Charges_LoyolaCDM',
    'https://smithtech.io/db_admin/columns/Charges_NorthShore',
    'https://smithtech.io/db_admin/columns/Charges_Rush',
    'https://smithtech.io/db_admin/columns/Charges_UCMC',
    'https://smithtech.io/db_admin/columns/Charges_Advocate',
]



convert_to_yaml_for_schema = [
    'https://smithtech.io/api/systems',
    'https://smithtech.io/api/systems/4',  # Example: Use an actual system_id that exists in your database.
    'https://smithtech.io/api/locations',
    'https://smithtech.io/api/locations/1',  # Example: Use an actual system_id that exists in your database.
    'https://smithtech.io/api/charges/system/4/location/27',  # Example: Use actual system_id and location_id values.
    'https://smithtech.io/react/eligibility/carriers',
    'https://smithtech.io/react/eligibility/carriers/1',
    'https://smithtech.io/react/eligibility/insurances',
    'https://smithtech.io/react/eligibility/insurances/1',
    'https://smithtech.io/react/eligibility/insurance-types',
    'https://smithtech.io/react/eligibility/insurance-types/1',
    'https://smithtech.io/react/eligibility/insurance-info/carrier/1',
    'https://smithtech.io/react/eligibility/insurance-plans/1',
    'https://smithtech.io/react/eligibility/records/system/1',
    'https://smithtech.io/react/eligibility/records/system/4/location/17',
    'https://smithtech.io/react/eligibility/network-info/1',
]


num_requests_per_endpoint = int(input("How many times do you want to test each endpoint? "))

# Concurrent requests
concurrent_requests = 5

def make_request(url):
    start_time = time()
    response = requests.get(url)
    response_time = time() - start_time
    return response.status_code, response_time

def test_endpoint(url, csv_writer):
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        future_to_request = {executor.submit(make_request, url): i for i in range(num_requests_per_endpoint)}
        response_times = []
        status_codes = []

        for future in concurrent.futures.as_completed(future_to_request):
            request_number = future_to_request[future] + 1
            status_code, response_time = future.result()

            response_times.append(response_time)
            status_codes.append(status_code)

            csv_writer.writerow([url, request_number, status_code, f"{response_time:.4f}"])
            print(f"Request {request_number} for {url} returned status code {status_code} in {response_time:.4f} seconds.")
    
    avg_response_time = mean(response_times)
    csv_writer.writerow(['', 'Average', '', f"{avg_response_time:.4f}"])
    csv_writer.writerow([])  # Add a blank row for spacing

    return response_times, status_codes, avg_response_time

# Get current timestamp
current_timestamp = strftime('%Y-%m-%d_%H-%M-%S')

# Write results to CSV and summarize in text file
summary_results = []
csv_filename = f'test_results/web_results_{current_timestamp}.csv'
txt_filename = f'test_results/web_summary_{current_timestamp}.txt'

with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for endpoint in endpoints:
        response_times, status_codes, avg_response_time = test_endpoint(endpoint, csv_writer)
        summary_results.append((endpoint, response_times, status_codes, avg_response_time))

# Write summary to text file
with open(txt_filename, 'w') as text_file:
    for endpoint, response_times, status_codes, avg_response_time in summary_results:
        text_file.write(f"Endpoint: {endpoint}\n")
        text_file.write(f"Total Requests: {len(response_times)}\n")
        text_file.write(f"Average Response Time: {avg_response_time:.4f} seconds\n")
        text_file.write(f"Status Codes: {', '.join(map(str, set(status_codes)))}\n")
        text_file.write(f"Max Response Time: {max(response_times):.4f} seconds\n")
        text_file.write(f"Min Response Time: {min(response_times):.4f} seconds\n\n")

print("Testing completed.")


