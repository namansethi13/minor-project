import pandas as pd

# Create a sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Add a new column with the same name
new_column_name = 'Name'
new_column_values = ['David', 'Eve', 'Frank']

# Method 1: Using square bracket notation
df[new_column_name] = new_column_values

# Method 2: Using the assign method
df = df.assign(**{new_column_name: new_column_values})

# Display the DataFrame after adding the column
print("\nDataFrame with the new column:")
print(df)
