import pandas as pd
import os

# Get the current directory
current_directory = os.getcwd()

# File paths
hospital_insurance_path = os.path.join(current_directory, 'hospital_insurance_plans.xlsx')
carriers_mapping_path = os.path.join(current_directory, 'CarriersMapping.xlsx')

# Load the data
hospital_insurance_df = pd.read_excel(hospital_insurance_path)
carriers_mapping_df = pd.read_excel(carriers_mapping_path)

# Create a dictionary from the carriers mapping dataframe
carriers_dict = dict(zip(carriers_mapping_df['CarrierID'], carriers_mapping_df['CarrierName']))

# Map the CarrierName to the insurance plans dataframe
hospital_insurance_df['CarrierName'] = hospital_insurance_df['CarrierID'].map(carriers_dict)

# Define the path for the new Excel file
updated_hospital_insurance_path = os.path.join(current_directory, 'updated_hospital_insurance_plans.xlsx')

# Save the updated dataframe to a new Excel file
hospital_insurance_df.to_excel(updated_hospital_insurance_path, index=False)

print("Carrier names updated successfully and saved in 'updated_hospital_insurance_plans.xlsx'.")
