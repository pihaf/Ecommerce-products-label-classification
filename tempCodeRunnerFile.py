for value in result_dict:
    df.loc[df['Product Name'].str.contains(value), 'Label'] = value

df.to_csv('df3.csv', index=False)
print("Done")