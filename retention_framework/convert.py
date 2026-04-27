import pandas as pd

# Target specific worksheet bypassing the dictionary
df = pd.read_excel('data/E Commerce Dataset.xlsx', sheet_name='E Comm')
df.to_csv('data/E Commerce Dataset.csv', index=False)