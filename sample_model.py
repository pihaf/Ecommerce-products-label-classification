import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.metrics import Recall, Precision, F1Score

def df_to_excel(df, output_file_path, sheet_name):
    with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)  

def excel_to_df(input_file_path, sheet_name):
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)
    return df

# data = excel_to_df('main/validation_data.xlsx', 'test_data')
data = pd.read_csv('final_data.csv')

# Splitting labels and text descriptions
labels = data['Label'].values
descriptions = data['Product Name'].values

# Combine training and test data into a single DataFrame
combined_data = pd.DataFrame({'Label': labels, 'Product Name': descriptions})

# Replace NaN values with empty strings
combined_data['Product Name'] = combined_data['Product Name'].fillna('')

# Apply label encoding to the combined data
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(combined_data['Label'])

# Splitting data into train and test sets
train_data, test_data, train_labels, test_labels = train_test_split(
    combined_data, encoded_labels, test_size=0.2, random_state=42)

# Creating a tokenizer and fitting it on the training text descriptions
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data['Product Name'])

# Converting training and testing text descriptions to sequences of integers
train_sequences = tokenizer.texts_to_sequences(train_data['Product Name'])
test_sequences = tokenizer.texts_to_sequences(test_data['Product Name'])

# Padding sequences to have the same length
max_length = max([len(seq) for seq in train_sequences + test_sequences])
train_padded_sequences = pad_sequences(train_sequences, maxlen=max_length)
test_padded_sequences = pad_sequences(test_sequences, maxlen=max_length)

# Converting labels to one-hot encoded vectors
num_classes = len(label_encoder.classes_)
train_labels_one_hot = keras.utils.to_categorical(train_labels, num_classes=num_classes)
test_labels_one_hot = keras.utils.to_categorical(test_labels, num_classes=num_classes)

# Creating the Keras model
model = keras.Sequential()
model.add(keras.layers.Embedding(len(tokenizer.word_index) + 1, 100, input_length=max_length))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(num_classes, activation='softmax'))

# Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', Recall, Precision, F1Score])

# Training the model
model.fit(train_padded_sequences, train_labels_one_hot, epochs=10, batch_size=32)

# Saving the model to a file
model.save('model.h5')

# Evaluating the model on the test data
test_loss, test_accuracy = model.evaluate(test_padded_sequences, test_labels_one_hot)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# Predicting on new data
validation_data = pd.read_csv('validation_data.csv')
true_labels = validation_data['Label'].values
new_sequences = tokenizer.texts_to_sequences(validation_data['Product Name'])
new_padded_sequences = pad_sequences(new_sequences, maxlen=max_length)
predictions = model.predict(new_padded_sequences)
predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

# Evaluating accuracy and loss on new data
#new_loss, new_accuracy = model.evaluate(new_padded_sequences, keras.utils.to_categorical(true_labels, num_classes=num_classes))

# Calculating recall, precision, and F1 score on new data
new_recall = recall_score(true_labels, predicted_labels, average='weighted')
new_precision = precision_score(true_labels, predicted_labels, average='weighted')
new_f1score = f1_score(true_labels, predicted_labels, average='weighted')
micro_f1 = f1_score(true_labels, predicted_labels, average='micro')

print("Recall after predicting: ")
print(new_recall)
print("Precision after predicting: ")
print(new_precision)
print("F1 Score after predicting: ")
print(new_f1score)
print("Micro F1:")
print(micro_f1)

# Print predicted labels to a file
product_name = validation_data['Product Name']
temp_list = product_name.values.tolist()
results = pd.DataFrame({'Label': predicted_labels, 'Product Name': temp_list})

# Write the result dataframe to a new file
results.to_csv('predicted_labels.csv', index=False)
