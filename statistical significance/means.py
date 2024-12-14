import pandas as pd
from scipy import stats
import csv

def calculate_means(file_path):
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

    # Define the cutoff date
    cutoff_date = pd.to_datetime('2022-08', format='%Y-%m')

    # Calculate the overall means and standard deviations
    overall_mean_positive = filtered_data['Percent Positive'].mean()
    overall_std_positive = filtered_data['Percent Positive'].std()
    overall_mean_negative = filtered_data['Percent Negative'].mean()
    overall_std_negative = filtered_data['Percent Negative'].std()
    overall_mean_neutral = filtered_data['Percent Neutral'].mean()
    overall_std_neutral = filtered_data['Percent Neutral'].std()

    # Filter the data for the date range
    range_data = filtered_data[filtered_data['Year-Month'] >= cutoff_date]

    # Calculate the means and standard deviations for the date range
    range_mean_positive = range_data['Percent Positive'].mean()
    range_std_positive = range_data['Percent Positive'].std()
    range_mean_negative = range_data['Percent Negative'].mean()
    range_std_negative = range_data['Percent Negative'].std()
    range_mean_neutral = range_data['Percent Neutral'].mean()
    range_std_neutral = range_data['Percent Neutral'].std()

    # Perform a t-test to compare the means
    t_stat_positive, p_value_positive = stats.ttest_ind(filtered_data['Percent Positive'], range_data['Percent Positive'])
    t_stat_negative, p_value_negative = stats.ttest_ind(filtered_data['Percent Negative'], range_data['Percent Negative'])
    t_stat_neutral, p_value_neutral = stats.ttest_ind(filtered_data['Percent Neutral'], range_data['Percent Neutral'])

    return {
        'file': file_path,
        'overall_mean_positive': overall_mean_positive,
        'range_mean_positive': range_mean_positive,
        'std_positive': overall_std_positive,
        'range_std_positive': range_std_positive,
        't_stat_positive': t_stat_positive,
        'p_value_positive': p_value_positive,
        'overall_mean_negative': overall_mean_negative,
        'range_mean_negative': range_mean_negative,
        'std_negative': overall_std_negative,
        'range_std_negative': range_std_negative,
        't_stat_negative': t_stat_negative,
        'p_value_negative': p_value_negative,
        'overall_mean_neutral': overall_mean_neutral,
        'range_mean_neutral': range_mean_neutral,
        'std_neutral': overall_std_neutral,
        'range_std_neutral': range_std_neutral,
        't_stat_neutral': t_stat_neutral,
        'p_value_neutral': p_value_neutral
    }

# File paths
file_paths = ['Chicago Raw.csv', 'Denver Raw.csv', 'NY RAW.csv']

# Collect results
results = []
for file_path in file_paths:
    result = calculate_means(file_path)
    results.append(result)

# Write results to CSV
with open('means_comparison_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for result in results:
        writer.writerow([f"Results for {result['file']}"])
        writer.writerow(['Statistic', 'Positive', 'Negative', 'Neutral'])
        writer.writerow(['Overall Mean', result['overall_mean_positive'], result['overall_mean_negative'], result['overall_mean_neutral']])
        writer.writerow(['Range Mean', result['range_mean_positive'], result['range_mean_negative'], result['range_mean_neutral']])
        writer.writerow(['Overall Std Dev', result['std_positive'], result['std_negative'], result['std_neutral']])
        writer.writerow(['Range Std Dev', result['range_std_positive'], result['range_std_negative'], result['range_std_neutral']])
        writer.writerow(['T-Stat', result['t_stat_positive'], result['t_stat_negative'], result['t_stat_neutral']])
        writer.writerow(['P-Value', result['p_value_positive'], result['p_value_negative'], result['p_value_neutral']])
        writer.writerow([])  # Empty row for separation