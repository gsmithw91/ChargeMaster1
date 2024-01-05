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
    'http://127.0.0.1:5000/api/systems',
    'http://127.0.0.1:5000/api/systems/1',  # Example: Use an actual system_id that exists in your database.
    'http://127.0.0.1:5000/api/locations',
    'http://127.0.0.1:5000/api/locations/1',  # Example: Use an actual system_id that exists in your database.
    'http://127.0.0.1:5000/api/charges/system/4/location/27',  # Example: Use actual system_id and location_id values.
    'http://127.0.0.1:5000/react/eligibility/carriers',
    'http://127.0.0.1:5000/react/eligibility/carriers/1',
    'http://127.0.0.1:5000/react/eligibility/insurances',
    'http://127.0.0.1:5000/react/eligibility/insurances/1',
    'http://127.0.0.1:5000/react/eligibility/insurance-types',
    'http://127.0.0.1:5000/react/eligibility/insurance-types/1',
    'http://127.0.0.1:5000/react/eligibility/insurance-info/carrier/1',
    'http://127.0.0.1:5000/react/eligibility/records/system/4/location/17',
    'http://127.0.0.1:5000/react/eligibility/records/system/4',
    'http://127.0.0.1:5000/react/eligibility/network-info/1',
    'http://127.0.0.1:5000/react/locations/details/1'
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
csv_filename = f'test_results/results_{current_timestamp}.csv'
txt_filename = f'test_results/summary_{current_timestamp}.txt'

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


