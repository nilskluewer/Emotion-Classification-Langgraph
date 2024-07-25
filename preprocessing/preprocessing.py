# Merge csv Posting and Votes
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv(r'./data/raw_csv/Postings_01052019_31052019.csv')

# Display the first 10 rows
print(df.head(10).to_string())