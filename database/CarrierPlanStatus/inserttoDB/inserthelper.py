import pandas as pd
import csv
import pandas as pd 

data = pd.read_csv('CarriersPlans.csv')

unique_carriers = data['Carrier'].unique()
unique_names = data['PlanName'].unique()
unique_insurance = data['InsuranceType'].unique()

carrier_mapping = {
    'Aetna': 1,
    'MultiPlan-PHCS': 2,
    'Blue Cross Blue Shield': 3,
    'Cigna': 4,
    'ComPsych': 5,
    'Coventry': 6,
    'Curaechoice': 7,
    'Global Excel': 8,
    'Health Alliance': 9,
    'HFN': 10,
    'Humana': 11,
    'Imagine Health': 12,
    'The Alliance': 13,
    'Optum': 14,
    'United Healthcare': 15,
    'CHAMPUS': 16,
    'Medicare': 17,
    'Medicaid': 18,
    'VA': 19,
    'Tricare East': 20,
    'United': 21,
    'United HealthCare': 22,
    'Zing': 23,
    'CountyCare': 24,
    'Meridian': 25
    # Continue adding the rest of the carriers and IDs as needed
}
insurance_type_mapping = {
    'Commercial': 1,
    'Government': 2,
    'Exchange': 3,
    'Medicaid': 4,
    'Medicare': 5,
    'Managed Medicaid': 7,
    'Medicare Advantage': 8,
    'Medicare/Medicaid Initiative (MMAI)': 9
}



def insert_elig_table():

    # Assuming the CSV file is named 'data.csv' and is in the same directory as this script
    
    # Replace with the actual path to your CSV file
    csv_file_path = 'CarriersPlans.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Generate SQL INSERT statements
    insert_statements = []
    for index, row in df.iterrows():
        # Handle potential single quote in PlanName by replacing single quote with two single quotes
        plan_name = row['PlanName'].replace("'", "''")
        insert_statements.append(f"INSERT INTO dbo.Elig_Northwestern (SystemID, LocationID, InsuranceTypeID, Carrier, PlanName, EligibilityYear) VALUES ({row['SystemID']}, {row['LocationID']}, {row['InsuranceTypeID']}, '{row['Carrier']}', '{plan_name}', {row['EligibilityYear']});")

    # Write the SQL statements to a file
    sql_file_path = 'insert_statements.sql'
    with open(sql_file_path, 'w') as file:
        file.write('\n'.join(insert_statements))

print(unique_carriers)
print(unique_names)
print(unique_insurance)
insert_elig_table()