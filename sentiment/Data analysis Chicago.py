import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Read the CSV file
file_path = '../statistical significance/NY RAW.csv'
data = pd.read_csv(file_path)

# Convert relevant columns to numeric types
data['Percent Positive'] = pd.to_numeric(data['Percent Positive'], errors='coerce')
data['Percent Negative'] = pd.to_numeric(data['Percent Negative'], errors='coerce')
data['Percent Neutral'] = pd.to_numeric(data['Percent Neutral'], errors='coerce')

# Extract the relevant columns
year_month = data['Year-Month']
percent_positive = data['Percent Positive']
percent_negative = data['Percent Negative']
percent_neutral = data['Percent Neutral']

# Filter out points that are equal to 0 or 1 or are undefined
filtered_data = data[(data['Percent Positive'] > 0) & (data['Percent Positive'] < 1) &
                     (data['Percent Negative'] > 0) & (data['Percent Negative'] < 1) &
                     (data['Percent Neutral'] > 0) & (data['Percent Neutral'] < 1)]

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Year-Month'], filtered_data['Percent Positive'], color='blue', alpha=0.5, label='Percent Positive')
plt.scatter(filtered_data['Year-Month'], filtered_data['Percent Negative'], color='red', alpha=0.5, label='Percent Negative')
plt.scatter(filtered_data['Year-Month'], filtered_data['Percent Neutral'], color='yellow', alpha=0.5, label='Percent Neutral')
plt.title('Scatter Plot of Comments per Month')
plt.xlabel('Year-Month')
plt.ylabel('Percent')
plt.legend()

# Set x-axis labels to show fewer labels
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
plt.xticks(rotation=45)

# Set y-axis to stretch from 0 to 1 with regular intervals of 0.1
plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=11))
plt.ylim(0, 1)

plt.grid(True)
plt.tight_layout()

# Save the plot as an image file
plt.savefig('NY_Comments_Scatter_Plot_All_Time.png')

# Show the plot
plt.show()