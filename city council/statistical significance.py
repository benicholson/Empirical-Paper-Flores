import pandas as pd
from scipy.stats import chi2_contingency

# Read the CSV file
file_path = 'city_council_analysis_results.csv'
data = pd.read_csv(file_path)

# Extract the 'Approve by Race' and 'Oppose by Race' columns
approve_by_race = eval(data.loc[data['Metric'] == 'Count', 'Approve by Race'].values[0])
oppose_by_race = eval(data.loc[data['Metric'] == 'Count', 'Oppose by Race'].values[0])

# Convert percentages to counts (assuming total counts are known)
total_approve = data.loc[data['Metric'] == 'Count', 'Approve Count'].values[0]
total_oppose = data.loc[data['Metric'] == 'Count', 'Oppose Count'].values[0]

approve_counts_race = {race: (percent / 100) * total_approve for race, percent in approve_by_race.items()}
oppose_counts_race = {race: (percent / 100) * total_oppose for race, percent in oppose_by_race.items()}

# Create a contingency table for race
races = set(approve_counts_race.keys()).union(set(oppose_counts_race.keys()))
contingency_table_race = [[approve_counts_race.get(race, 0), oppose_counts_race.get(race, 0)] for race in races]

# Perform the chi-square test for race
chi2_race, p_race, dof_race, expected_race = chi2_contingency(contingency_table_race)

# Extract the 'Approve by Age' and 'Oppose by Age' columns
approve_by_age = eval(data.loc[data['Metric'] == 'Count', 'Approve by Age'].values[0])
oppose_by_age = eval(data.loc[data['Metric'] == 'Count', 'Oppose by Age'].values[0])

# Convert percentages to counts (assuming total counts are known)
approve_counts_age = {age: (percent / 100) * total_approve for age, percent in approve_by_age.items()}
oppose_counts_age = {age: (percent / 100) * total_oppose for age, percent in oppose_by_age.items()}

# Create a contingency table for age
ages = set(approve_counts_age.keys()).union(set(oppose_counts_age.keys()))
contingency_table_age = [[approve_counts_age.get(age, 0), oppose_counts_age.get(age, 0)] for age in ages]

# Perform the chi-square test for age
chi2_age, p_age, dof_age, expected_age = chi2_contingency(contingency_table_age)

# Extract the 'Approve by Tag' and 'Oppose by Tag' columns
approve_by_tag = eval(data.loc[data['Metric'] == 'Count', 'Approve by Tag'].values[0])
oppose_by_tag = eval(data.loc[data['Metric'] == 'Count', 'Oppose by Tag'].values[0])

# Convert percentages to counts (assuming total counts are known)
approve_counts_tag = {tag: (percent / 100) * total_approve for tag, percent in approve_by_tag.items()}
oppose_counts_tag = {tag: (percent / 100) * total_oppose for tag, percent in oppose_by_tag.items()}

# Create a contingency table for tags
tags = set(approve_counts_tag.keys()).union(set(oppose_counts_tag.keys()))
contingency_table_tag = [[approve_counts_tag.get(tag, 0), oppose_counts_tag.get(tag, 0)] for tag in tags]

# Perform the chi-square test for tags
chi2_tag, p_tag, dof_tag, expected_tag = chi2_contingency(contingency_table_tag)

# Create a DataFrame to store the results
results = pd.DataFrame({
    'Test': ['Race', 'Age', 'Tag'],
    'Chi-square statistic': [chi2_race, chi2_age, chi2_tag],
    'P-value': [p_race, p_age, p_tag],
    'Degrees of freedom': [dof_race, dof_age, dof_tag],
    'Expected frequencies': [expected_race.tolist(), expected_age.tolist(), expected_tag.tolist()]
})

# Save the results to a CSV file
results.to_csv('chi_square_test_results.csv', index=False)

print("Chi-square test results have been saved to 'chi_square_test_results.csv'")