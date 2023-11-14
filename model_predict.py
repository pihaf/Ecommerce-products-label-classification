import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

validation_data = pd.read_csv('validation_data.csv')

validation_labels = validation_data['Label'].values
validation_descriptions = validation_data['Product Name'].values

model = keras.models.load_model('model.h5')

# Load the tokenizer and max_length
tokenizer = Tokenizer()
max_length = model.input_shape[1]

# Load the label_encoder
label_encoder_path = 'label_encoder.pkl'
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load(label_encoder_path, allow_pickle=True)

validation_sequences = tokenizer.texts_to_sequences(validation_descriptions)
validation_padded_sequences = pad_sequences(validation_sequences, maxlen=max_length)

predictions = model.predict(validation_padded_sequences)
predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

# Print predicted labels to a file
product_name = validation_data['Product Name']
temp_list = product_name.values.tolist()
results = pd.DataFrame({'Label': predicted_labels, 'Product Name': temp_list})

# Write the result dataframe to a new file
results.to_csv('predicted_labels.csv', index=False)