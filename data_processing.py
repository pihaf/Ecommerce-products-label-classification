import pandas as pd

def df_to_excel(df, output_file_path, sheet_name):
    with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)  

def excel_to_df(input_file_path, sheet_name):
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)
    return df

def find_different_labels(df1, df2, column1, column2):
    # Extract the unique values of the column from both dataframes
    df1_values = set(df1[column1].unique())
    df2_values = set(df2[column2].unique())

    # Find the values in df2 that are not in df1
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
validation_data = pd.read_csv('main/validation_data.csv')
final_data = pd.read_csv('main/final_data.csv')

# Total labels of data
print('Total labels: ' + str(validation_data['Label'].nunique()))
print('Total labels: ' + str(final_data['Label'].nunique()))

# columns = ['link1', 'link2', 'title']
# new_data = data[columns]
# new_data = new_data.copy()
# new_data['link1'] = new_data['link1'].str.replace('"', '')
# new_data['link2'] = new_data['link2'].str.replace('"', '')
# new_data['title'] = new_data['title'].str.replace('"', '')
# print(new_data.head())
# new_data.to_csv('new_data.csv', index=False)

# Check for duplicates
# duplicate_rows = final_data[final_data.duplicated()]
# duplicate_count = duplicate_rows.shape[0]
# print(duplicate_count)

# Remove duplicates
# df_unique = final_data.drop_duplicates()
# df_unique.to_csv('final_Data.csv', index=False)

# Check for different and common labels
common_labels = find_common_labels(validation_data, final_data, 'Label', 'Label')
print('Total common labels: ' + str(len(common_labels)))
print(common_labels)
# print('Total different labels: ')
# print(find_different_labels(validation_data, data, 'Label', 'link2'))
