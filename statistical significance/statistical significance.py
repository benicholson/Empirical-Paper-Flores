import pandas as pd
from scipy import stats

# Read the CSV file
file_path = 'NY Raw.csv'
data = pd.read_csv(file_path)

# Convert relevant columns to numeric types
data['Percent Positive'] = pd.to_numeric(data['Percent Positive'], errors='coerce')
data['Percent Negative'] = pd.to_numeric(data['Percent Negative'], errors='coerce')
data['Percent Neutral'] = pd.to_numeric(data['Percent Neutral'], errors='coerce')
data['Total Comments'] = pd.to_numeric(data['Total Comments'], errors='coerce')

# Filter out points that are equal to 0 or 1 or are undefined
filtered_data = data[(data['Percent Positive'] > 0) & (data['Percent Positive'] < 1) &
                     (data['Percent Negative'] > 0) & (data['Percent Negative'] < 1) &
                     (data['Percent Neutral'] > 0) & (data['Percent Neutral'] < 1)].copy()

# Convert 'Year-Month' to datetime
filtered_data.loc[:, 'Year-Month'] = pd.to_datetime(filtered_data['Year-Month'], format='%Y-%m')

# Filter the data for the specified date range (2022-08 to 2024-12)
start_date = pd.to_datetime('2022-08', format='%Y-%m')
end_date = pd.to_datetime('2024-12', format='%Y-%m')
date_range_data = filtered_data[(filtered_data['Year-Month'] >= start_date) & (filtered_data['Year-Month'] <= end_date)]

# Calculate the overall mean and standard deviation of the percent of negative, positive, and neutral comments
overall_mean_positive = filtered_data['Percent Positive'].mean()
overall_std_positive = filtered_data['Percent Positive'].std()
overall_mean_negative = filtered_data['Percent Negative'].mean()
overall_std_negative = filtered_data['Percent Negative'].std()
overall_mean_neutral = filtered_data['Percent Neutral'].mean()
overall_std_neutral = filtered_data['Percent Neutral'].std()

# Calculate the mean and standard deviation of the percent of negative, positive, and neutral comments for the specified date range
date_range_mean_positive = date_range_data['Percent Positive'].mean()
date_range_std_positive = date_range_data['Percent Positive'].std()
date_range_mean_negative = date_range_data['Percent Negative'].mean()
date_range_std_negative = date_range_data['Percent Negative'].std()
date_range_mean_neutral = date_range_data['Percent Neutral'].mean()
date_range_std_neutral = date_range_data['Percent Neutral'].std()

# Perform a t-test to compare the means
t_stat_positive, p_value_positive = stats.ttest_1samp(date_range_data['Percent Positive'], overall_mean_positive)
t_stat_negative, p_value_negative = stats.ttest_1samp(date_range_data['Percent Negative'], overall_mean_negative)
t_stat_neutral, p_value_neutral = stats.ttest_1samp(date_range_data['Percent Neutral'], overall_mean_neutral)

# Create a DataFrame to store the results
results = pd.DataFrame({
    'Metric': ['Mean', 'Standard Deviation', 'T-Statistic', 'P-Value'],
    'Percent Positive': [overall_mean_positive, overall_std_positive, t_stat_positive, p_value_positive],
    'Percent Negative': [overall_mean_negative, overall_std_negative, t_stat_negative, p_value_negative],
    'Percent Neutral': [overall_mean_neutral, overall_std_neutral, t_stat_neutral, p_value_neutral]
})

# Save the results to a CSV file
results.to_csv('NY_statistical_significance_results.csv', index=False)

print("Results have been saved to 'NY_statistical_significance_results.csv'")