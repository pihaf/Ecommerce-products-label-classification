import pandas as pd

def df_to_excel(df, output_file_path, sheet_name):
    with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)  

def excel_to_df(input_file_path, sheet_name):
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)
    return df

def txt_to_csv(input_file, outputfile):
    # Read the text file into a DataFrame
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    labels = []
    products = []
    for line in data:
        parts = line.split(' ', 1)  # Split into two parts: label and product name
        if len(parts) == 2:
            label, product_name = parts
            label = label.replace('__label__', '').replace('_', ' ')
            labels.append(label.strip())
            products.append(product_name.strip())
    
    df = pd.DataFrame({'Label': labels, 'Product Name': products})
    df.to_csv(outputfile, index=False)

def csv_to_txt(input_file, output_file):
    # Read the CSV file into a dataframe
    df = pd.read_csv(input_file)

    # Iterate through each row of the dataframe
    with open(output_file, 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            value1 = str(row['Label']) 
            value2 = str(row['Product Name'])
            new_value1 = value1.replace(' ', '_')
            line = f"__label__{new_value1} {value2}\n"
            
            # Write the line to the text file
            f.write(line)

def find_different_labels(df1, df2, column1, column2):
    # Extract the unique values of the column from both dataframes
    df1_values = set(df1[column1].unique())
    df2_values = set(df2[column2].unique())

    # Find the values in df1 that are not in df2
    different_values = df1_values.difference(df2_values)

    return different_values

def find_common_labels(df1, df2, column1, column2):
    # Get the unique values of column1 from df1
    df1_values = set(df1[column1].unique())
    df2_values = set(df2[column2].unique())
    
    # Find the common values
    common_values = df1_values.intersection(df2_values)
    
    return common_values

# Get data from files
validation_data = pd.read_csv('data/validation_data.csv')
final_data = pd.read_csv('data/final_products_vg.csv')
full_data = pd.read_csv('data/full_products_vg.csv')

# Total labels of data
print('Total labels: ' + str(validation_data['Label'].nunique()))
print('Total labels: ' + str(final_data['Label'].nunique()))

#csv_to_txt('predicted_labels_final.csv', 'nhom10_sol3.txt')

# Check for NaN
# print("Rows with NaN values:")
# print(final_data[final_data.isna().any(axis=1)])

# Remove rows containing NaN values
# final_data = final_data.dropna()

# Check for duplicates
# duplicate_rows = final_data[final_data.duplicated()]
# duplicate_count = duplicate_rows.shape[0]
# print(duplicate_count)

# Remove duplicates
# df_unique = final_data.drop_duplicates()
# df_unique.to_csv('final_products_vg.csv', index=False)

# Check for common labels
common_labels = find_common_labels(validation_data, final_data, 'Label', 'Label')
print('Total common labels: ' + str(len(common_labels)))

# Check for different labels
different_labels = find_different_labels(final_data, validation_data, 'Label', 'Label')
print('Total missing labels: ' + str(len(different_labels)))

# Remove data that have different labels than validation data
# final_data = final_data[~final_data['Label'].isin(different_labels)]
# final_data.to_csv('final_products_vg.csv', index=False)

# Write missing labels to a file
# with open("missing_labels.txt", "w", encoding='utf-8') as file:
#     for element in missing_labels:
#         file.write(element + "\n")
