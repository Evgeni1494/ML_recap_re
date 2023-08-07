import pandas as pd
import ast
import numpy as np

# Load the CSV files
join1_df = pd.read_csv('analyse.csv')
allocine_join2_df = pd.read_csv('allocine(1).csv')


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
data['acteur3'] = data['acteurs'].apply(lambda x: x[2] if len(x) > 2 else None)
# Convert 'nbre_entrees' from string to integer
data['nbre_entrees'] = data['nbre_entrees'].str.replace(' ', '').astype(int)

# Calculate the total number of entries for each director

entries_by_director = data.groupby('directeur')['nbre_entrees'].sum()

# Comptez le nombre de fois où chaque directeur apparaît dans les lignes du DataFrame
director_counts = data['directeur'].value_counts()

# Divisez la somme des entrées par le nombre de fois où le directeur apparaît
result = entries_by_director / director_counts
# Calculate 'director_success' as a score out of 10 based on the total number of entries for each director
# director_success = (entries_by_director / entries_by_director.max() * 10).rename('director_success')
# print(entries_by_director.max())
# Update 'director_success' in the main DataFrame. If director is not present, set 'director_success' to 0.
data['director_moy_entr'] = data['directeur'].map(result).fillna(0)

# Convert 'note_presse' to float and 'prix' to int
data['note_presse'] = pd.to_numeric(data['note_presse'].str.replace(',', '.'), errors='coerce')
data['prix'] = pd.to_numeric(data['prix'], errors='coerce')

# Convert 'durée' to numeric minutes
data['durée'] = data['durée'].str.split('h').apply(lambda x: int(x[0])*60 + int(x[1]) if len(x) == 2 else int(x[0]))

# Drop rows where 'budget_def' is missing
data = data.dropna(subset=['budget_def'])

# Reset the index
data = data.reset_index(drop=True)

# Save the resulting DataFrame to a new CSV file
data.to_csv('PIPELINE_TEST3.csv', index=False)
