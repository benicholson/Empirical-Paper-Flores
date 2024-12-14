import pandas as pd

# Read the CSV file
file_path = 'city council counts.csv'
data = pd.read_csv(file_path)

# Filter out rows with 'NU' and 'N/A' in 'Approve of immigration?'
filtered_data = data[data['Approve of immigration?'].isin(['Y', 'N'])]

# Count the number of people who approved and opposed immigration
approve_count = filtered_data['Approve of immigration?'].value_counts().get('Y', 0)
oppose_count = filtered_data['Approve of immigration?'].value_counts().get('N', 0)

# Calculate the total number of people who responded
total_responses = approve_count + oppose_count

# Calculate the percentage of people who supported immigration
percent_support = (approve_count / total_responses) * 100 if total_responses > 0 else 0

# Count the total number of people for each race
race_counts = data['Race'].value_counts()

# Calculate the percentage of people who approved or opposed immigration by race
approve_by_race = filtered_data[filtered_data['Approve of immigration?'] == 'Y']['Race'].value_counts(normalize=True) * 100
oppose_by_race = filtered_data[filtered_data['Approve of immigration?'] == 'N']['Race'].value_counts(normalize=True) * 100

# Count the total number of people for each age group
age_counts = data['Age'].value_counts()

# Calculate the percentage of people who approved or opposed immigration by age group
approve_by_age = filtered_data[filtered_data['Approve of immigration?'] == 'Y']['Age'].value_counts(normalize=True) * 100
oppose_by_age = filtered_data[filtered_data['Approve of immigration?'] == 'N']['Age'].value_counts(normalize=True) * 100

# Calculate the percentage of people who approved or opposed immigration by tag
tags_series = filtered_data['Tags'].str.split(',').explode().str.strip()
approve_tags = tags_series[filtered_data['Approve of immigration?'] == 'Y'].value_counts(normalize=True) * 100
oppose_tags = tags_series[filtered_data['Approve of immigration?'] == 'N'].value_counts(normalize=True) * 100

# Calculate the general percentage of speakers mentioning each tag
general_tags = data['Tags'].str.split(',').explode().str.strip().value_counts(normalize=True) * 100

# Create a DataFrame to store the results
results = pd.DataFrame({
    'Metric': ['Count', 'Percentage'],
    'Approve Count': [approve_count, percent_support],
    'Oppose Count': [oppose_count, 100 - percent_support],
    'Race Counts': [race_counts.to_dict(), ''],
    'Approve by Race': [approve_by_race.to_dict(), ''],
    'Oppose by Race': [oppose_by_race.to_dict(), ''],
    'Age Counts': [age_counts.to_dict(), ''],
    'Approve by Age': [approve_by_age.to_dict(), ''],
    'Oppose by Age': [oppose_by_age.to_dict(), ''],
    'Approve by Tag': [approve_tags.to_dict(), ''],
    'Oppose by Tag': [oppose_tags.to_dict(), ''],
    'General Tags': [general_tags.to_dict(), '']
})

# Save the results to a CSV file
results.to_csv('city_council_analysis_results2.csv', index=False)

print("Results have been saved to 'city_council_analysis_results.csv'")