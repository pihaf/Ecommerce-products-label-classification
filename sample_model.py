import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
#from sklearn.metrics import precision_score, recall_score, f1_score
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.metrics import Precision, Recall, F1Score

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
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the model
model.fit(train_padded_sequences, train_labels_one_hot, epochs=10, batch_size=32)

# Saving the model to a file
model.save('model.h5')

# Evaluating the model on the test data
test_loss, test_accuracy = model.evaluate(test_padded_sequences, test_labels_one_hot)

# Predicting on new data
validation_data = pd.read_csv('validation_data.csv')
new_sequences = tokenizer.texts_to_sequences(validation_data['Product Name'])
new_padded_sequences = pad_sequences(new_sequences, maxlen=max_length)
predictions = model.predict(new_padded_sequences)
predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

# Calculate additional metrics for the test data
# test_predictions = model.predict(test_padded_sequences)
# test_predicted_labels = label_encoder.inverse_transform(np.argmax(test_predictions, axis=1))
# classification_report = classification_report(test_labels, np.argmax(test_predictions, axis=1), target_names=label_encoder.classes_)
# test_precision = precision_score(test_labels, predicted_labels, average='weighted')
# test_recall = recall_score(test_labels, predicted_labels, average='weighted')
# test_f1 = f1_score(test_labels, predicted_labels, average='weighted')


print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)
# print("Test Precision:", test_precision)
# print("Test Recall:", test_recall)
# print("Test F1 Score:", test_f1 )
# print("Classification Report:", classification_report)
# print("Predicted Labels:", predicted_labels)
