import requests
from bs4 import BeautifulSoup
import pandas as pd 

tab_selected = ['commercial'] # 'exchange', 'government'
# Define the URL of the website you want to scrape
url_location_map = {'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/northwestern-memorial-hospital' : 27 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/lake-forest-hospital' : 22,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/central-dupage-hospital' : 17 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/northwestern-medical-group' :42 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/delnor-hospital' : 18 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/huntley-mchenry-woodstock-hospitals' : 21 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/kishwaukee-hospital' : 20 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/marianjoy' : 23 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/palos-hospital' : 25 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/palos-imaging-and-diagnostics' : 41 ,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/regional-medical-group' : 42,
       'https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/valley-west-hospital' : 43}      
       
       


# Function to get the Carrier ID, or return 'Other'
def get_carrier_id(carrier_name):
    return carriers_mapping.get(carrier_name, 'Other')


import requests
from bs4 import BeautifulSoup


# Tabs to be appended to each URL
tabs = ['commercial'] #, 'exchange', 'government'

# Open a single file for writing all contents

# Tabs and their corresponding InsuranceTypeID
tab_insurance_type_map = {'commercial': 1, 'exchange': 3}

# Initialize a list to hold all row data
data_rows = []

# Iterate over each URL and corresponding LocationID
for url, location_id in url_location_map.items():
    # For each tab you want to scrape
    for tab in tab_selected:
        # Construct the URL for the tab
        tab_url = f"{url}#{tab}"
        
        # Make a request to the tab URL
        response = requests.get(tab_url)
        response.raise_for_status()  # This will raise an error for a bad status
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the content you're interested in, here's an example of how you might do this:
        for paragraph in soup.find_all('p'):
            # Split the paragraph by line breaks or other markers
            insurance_plans = paragraph.get_text(separator="\n").split("\n")
            for plan in insurance_plans:
                plan = plan.strip()
                if plan:  # Check if the line is not empty
                    carrier_id = get_carrier_id(plan)
                    # Append a new row of data for each plan
                    data_rows.append({
                        'Eligibility ID': '',
                        'SystemID': 4,
                        'LocationID': location_id,
                        'InsuranceTypeID': 1 if tab == 'commercial' else 3 if tab == 'exchange' else '',
                        'CarrierID': carrier_id,
                        'Carrier': 'Other' if carrier_id == 'Other' else plan,
                        'InNetwork': 1,
                        'EligibilityYear': '',
                        'Plan Name': plan
                    })

# Convert list of row data into a pandas DataFrame
df = pd.DataFrame(data_rows)

# Save DataFrame to an Excel file
df.to_excel('hospital_insurance_plans.xlsx', index=False, engine='openpyxl')