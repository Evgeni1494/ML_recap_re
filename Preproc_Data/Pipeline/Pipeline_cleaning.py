import pandas as pd
import ast
import numpy as np

# Function to transform date to the required format
def transform_date(row):
    date_string = row['date']
    sortie_string = row['date_de_sortie']
    
    # Define a dictionary to map French month names to numbers
    month_dict = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08', 
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    
    # Check if the date is "00/00/0000"
    if date_string == "00/00/0000":
        # Replace French month names with numbers in sortie_string
        for month_name, month_number in month_dict.items():
            sortie_string = sortie_string.replace(month_name, month_number)

        # Convert the sortie date to the required format
        date = pd.to_datetime(sortie_string, format="%d %m %Y", errors='coerce')
    else:
        # Convert to datetime format
        date = pd.to_datetime(date_string, format="%d/%m/%Y", errors='coerce')
        
    # If the date conversion was successful
    if pd.notna(date):
        # Convert to ISO format and add the time
        date_iso = date.isoformat() + "Z"
    else:
        date_iso = None

    return date_iso





# Load the CSV files
join1_df = pd.read_csv('join1.csv')
allocine_join2_df = pd.read_csv('allocine_join2.csv')



# Data cleaning: remove leading/trailing spaces and convert to lower case
join1_df['title_clean'] = join1_df['title'].str.strip().str.lower()
allocine_join2_df['title_clean'] = allocine_join2_df['titre'].str.strip().str.lower()

# Perform the join operation
data = pd.merge(join1_df, allocine_join2_df, how='inner', left_on='title_clean', right_on='title_clean')

# Select and rename columns to match the structure of 'jointure.csv'
data = data[['title', 'nbre_entrees', 'title_original', 'distributeur', 'country', 'genre', 'date', 'public', 'durée',
             'date_de_sortie', 'directeur', 'acteurs', 'note_presse', 'box_office_france', 'prix', 'nominations', 'budget_y']]

data.columns = ['title', 'nbre_entrees', 'title_original', 'distributeur', 'country', 'genre', 'date', 'public', 'durée',
                'date_de_sortie', 'directeur', 'acteurs', 'note_presse', 'box_office_france', 'prix', 'nominations', 'budget_def']

# Convert 'acteurs' from string to list
data['acteurs'] = data['acteurs'].apply(ast.literal_eval)

# Extract 'acteur1' and 'acteur2'
data['acteur1'] = data['acteurs'].apply(lambda x: x[0] if len(x) > 0 else None)
data['acteur2'] = data['acteurs'].apply(lambda x: x[1] if len(x) > 1 else None)

data['acteur1'] = data['acteur1'].fillna('Unknown')
data['acteur2'] = data['acteur2'].fillna('Unknown')

# Calculate the total box office for each actor in 'acteur1' and 'acteur2'
entries_by_acteur1 = data.groupby('acteur1')['box_office_france'].sum()
entries_by_acteur2 = data.groupby('acteur2')['box_office_france'].sum()

# Calculate 'acteur1_success' and 'acteur2_success' as a score out of 10 based on the total box office for each actor
acteur1_success = (entries_by_acteur1 / entries_by_acteur1.max() * 10).rename('acteur1_success')
acteur2_success = (entries_by_acteur2 / entries_by_acteur2.max() * 10).rename('acteur2_success')

# Update 'acteur1_success' and 'acteur2_success' in the main DataFrame. If actor is not present or is 'Unknown', set the score to 0.
data['acteur1_success'] = data['acteur1'].map(acteur1_success).fillna(0)
data['acteur2_success'] = data['acteur2'].map(acteur2_success).fillna(0)

# Set the success score to 0 for 'Unknown' actors
data.loc[data['acteur1'] == 'Unknown', 'acteur1_success'] = 0
data.loc[data['acteur2'] == 'Unknown', 'acteur2_success'] = 0


# Convert 'nbre_entrees' from string to integer
data['nbre_entrees'] = data['nbre_entrees'].str.replace(' ', '').astype(int)

# Calculate the total number of entries for each director
entries_by_director = data.groupby('directeur')['box_office_france'].sum()

# Calculate 'director_success' as a score out of 10 based on the total number of entries for each director
director_success = (entries_by_director / entries_by_director.max() * 10).rename('director_success')

# Update 'director_success' in the main DataFrame. If director is not present, set 'director_success' to 0.
data['director_success'] = data['directeur'].map(director_success).fillna(0)

# Create 'cast_success' column as the average of 'director_success', 'acteur1_success' and 'acteur2_success'
data['cast_success'] = data[['director_success', 'acteur1_success', 'acteur2_success']].mean(axis=1)

# Convert 'note_presse' to float and 'prix' to int
data['note_presse'] = pd.to_numeric(data['note_presse'].str.replace(',', '.'), errors='coerce')
data['prix'] = pd.to_numeric(data['prix'], errors='coerce').fillna(0)

# Convert 'durée' to numeric minutes
data['durée'] = data['durée'].str.split('h').apply(lambda x: int(x[0])*60 + int(x[1]) if len(x) == 2 else int(x[0]))

# Drop rows where 'budget_def' is missing
data = data.dropna(subset=['budget_def'])

# Add 'id' column as an enumeration of the rows
data.reset_index(level=0, inplace=True)
data.rename(columns={"index": "id"}, inplace=True)

# Convert 'date' to the required format
data['date'] = data.apply(transform_date, axis=1)



# Save the resulting DataFrame to a new CSV file
data.to_csv('PIPELINE_TEST2.csv', index=False)
