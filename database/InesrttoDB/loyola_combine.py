import pandas as pd

# Load the data from both CSV files
loyola_charges = pd.read_csv('LoyolaCharges.csv')
loyola_cdm_charges = pd.read_csv('LoyolaCDMCharges.csv')

# Merge the two dataframes based on 'locationID' and 'billingCode'.
# This performs a left join by default, meaning all rows from loyola_charges will be included in the result.
# Where there are matching 'locationID' and 'billingCode' values, the columns from loyola_cdm_charges will be added.
# Where there are not, the new columns will contain NaN, which you can then replace with blanks if needed.
combined_data = pd.merge(loyola_charges, loyola_cdm_charges, how='left', on=['locationID', 'billingCode'])

# Drop duplicate columns (if any exist after the merge)
# This step is not strictly necessary as we specified the 'on' parameter in merge which only adds columns from the right dataframe that are not in the left dataframe, avoiding duplicates.
combined_data = combined_data.loc[:,~combined_data.columns.duplicated()]

# Replace NaN values with empty strings if you want blank cells where the values do not match
combined_data.fillna('', inplace=True)

# Save the combined data to a new CSV file
combined_data.to_csv('CombinedLoyolaCharges.csv', index=False)
