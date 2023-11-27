import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import numpy as np

# Load the training data from CSV file
train_data = pd.read_csv('final_data2.csv')
train_texts = train_data['Product Name']
train_labels = np.array(train_data['Label'])

# Load the validation data from CSV file
validation_data = pd.read_csv('validation_data.csv')
validation_texts = validation_data['Product Name']

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=8)

# Tokenize and encode training data
train_input_ids = []
train_attention_masks = []

for text in train_texts:
    encoded_text = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='tf',
    )
    train_input_ids.append(encoded_text['input_ids'][0])
    train_attention_masks.append(encoded_text['attention_mask'][0])

train_input_ids = np.array(train_input_ids)
train_attention_masks = np.array(train_attention_masks)

# Convert the training data into TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((train_input_ids, train_attention_masks, train_labels))

# Set batch size
batch_size = 8
train_dataset = train_dataset.shuffle(len(train_input_ids)).batch(batch_size)

# Compile the model with appropriate optimizer and loss function
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# Train the model
num_epochs = 3
model.fit(train_dataset, epochs=num_epochs)

# Tokenize and encode validation data
validation_input_ids = []
validation_attention_masks = []

for text in validation_texts:
    encoded_text = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='tf',
    )
    validation_input_ids.append(encoded_text['input_ids'][0])
    validation_attention_masks.append(encoded_text['attention_mask'][0])

validation_input_ids = np.array(validation_input_ids)
validation_attention_masks = np.array(validation_attention_masks)

# Create a TensorFlow dataset for validation data
validation_dataset = tf.data.Dataset.from_tensor_slices((validation_input_ids, validation_attention_masks))

# Predict labels for the validation data
validation_predictions = model.predict(validation_dataset)
validation_predicted_labels = np.argmax(validation_predictions, axis=1)

# Print the predicted labels for the validation data
for i, text in enumerate(validation_texts):
    predicted_label = validation_predicted_labels[i]
    print(f"Input: {text} | Predicted Label: {predicted_label}")