import pandas as pd 
import fuzzywuzzy
from fuzzywuzzy import fuzz

sheet_1_df = pd.read_excel('Elig_NW.xlsx',sheet_name='Sheet2')
sheet_2_df = pd.read_excel('Elig_NW.xlsx',sheet_name='Sheet3')

def find_best_match(plan_name, sheet2_df):
    best_match = None
    max_similarity = -1

    for index, row in sheet2_df.iterrows():
        similarity = fuzz.ratio(plan_name, row['PlanName'])
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = row['PlanID']

    return best_match

# Add a new column 'PlanID' to the first sheet with the closest matching PlanID
sheet_1_df['PlanID'] = sheet_1_df['PlanName'].apply(lambda x: find_best_match(x, sheet_2_df))

# Save the updated dataframe back to the Excel file
sheet_1_df.to_excel('Elig_NW_planID.xlsx', index=False)