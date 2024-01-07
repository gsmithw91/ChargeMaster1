import requests
from bs4 import BeautifulSoup
import csv

# The base URL for relative links
base_url = 'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans'

# List of hospital URLs (extracted from the HTML snippet)
hospital_urls = [
    # '/northwestern-memorial-hospital',
    '/lake-forest-hospital',
    # '/central-dupage-hospital',
    # '/northwestern-medical-group',
    # '/delnor-hospital',
    # '/huntley-mchenry-woodstock-hospitals',
    # '/kishwaukee-hospital',
    # '/marianjoy',
    # '/palos-hospital',
    # '/palos-imaging-and-diagnostics',
    # '/regional-medical-group',
    # '/valley-west-hospital',
]

# Function to scrape insurance plans
def scrape_insurance_plans(hospital_url):
    insurance_data = []
    # Define the types of insurance plans to scrape
    plan_types = ["Commercial", "Exchange", "Government"]
    
    # Loop through the types and append the plan type to the URL
    for plan_type in plan_types:
        url = f"{base_url}{hospital_url}#{plan_type}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the plan names and details here...
        # Find all divs with the class 'panel panel-alt' which contain the insurance info
        panels = soup.find_all('div', class_='panel panel-alt')
        for panel in panels:
            # Find the Carrier namec
            carrier = panel.find('h3')
            if carrier:
                carrier_name = carrier.text.strip()
                # Find all Plan names within the same panel
                plan_names = panel.find_all('p')
                for plan in plan_names:
                    insurance_data.append({
                        'LocationName': hospital_url.strip('/').replace('-', ' ').title(),
                        'EligibilityYear': '2023',  # Assuming the year is 2023
                        'InsuranceType': plan_type,
                        'Carrier': carrier_name,
                        'PlanName': plan.text.strip()
                    })
    return insurance_data

# Function to write data to CSV
def write_to_csv(data, file_path):
    # Write the data to a CSV file
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['LocationName', 'EligibilityYear', 'InsuranceType', 'Carrier', 'PlanName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the rows
        for entry in data:
            writer.writerow(entry)

# Prepare the data from all hospital URLs
all_insurance_data = []
for hospital_url in hospital_urls:
    all_insurance_data.extend(scrape_insurance_plans(hospital_url))

# Path for the new CSV file
new_csv_file_path = 'newInsurancePlans.csv'

# Write the scraped data to the new CSV file
write_to_csv(all_insurance_data, new_csv_file_path)
