import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import numpy as np

# Load the data from CSV file
data = pd.read_csv('main/final_data.csv')
samples = [
    ('Ghế văn phòng', 'Ghế HQ - HK095'),
    ('Thước dây', '30m Thước dây làm bằng sợi thủy tinh TOTAL TMTF12306'),
    ('Cưa tay', 'Cưa gỗ cầm tay cán lớn Asaki AK - 8657'),
    ('Váy, đầm', 'Đầm ren cổ V tay ngắn cao cấp'),
    ('Dụng cụ đo, kiểm tra khác', 'Máy đo độ đồng tâm HANN YAN 6401D1'),
    ('Linh kiện máy photocopy', 'Lô kéo giấy đẩy giấy ARDF SharpARM 256L / 316L / 318 / 258 / 5625 / 5726 / 5631 / M260 / 310 LKGDF310'),
    ('Bàn ghế trang điểm', 'Bàn trang điểm gỗ óc chó . BTH011'),
    ('Mobile', 'Điện thoại Wiko Robby 2G ( Gold )')
]

# Prepare labels and texts
labels = np.array(data['Label'])
texts = data['Product Name']

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=8)

# Tokenize and encode input texts
input_ids = []
attention_masks = []

for text in texts:
    encoded_text = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='tf',
    )
    input_ids.append(encoded_text['input_ids'][0])
    attention_masks.append(encoded_text['attention_mask'][0])

input_ids = np.array(input_ids)
attention_masks = np.array(attention_masks)

# Split the data into training and test sets
train_inputs, test_inputs = input_ids[:6], input_ids[6:]
train_masks, test_masks = attention_masks[:6], attention_masks[6:]
train_labels, test_labels = labels[:6], labels[6:]

# Convert the data into TensorFlow datasets
train_dataset = tf.data.Dataset.from_tensor_slices((train_inputs, train_masks, train_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_inputs, test_masks, test_labels))

# Set batch size and shuffle the training dataset
batch_size = 8
train_dataset = train_dataset.shuffle(len(train_inputs)).batch(batch_size)

# Compile the model with appropriate optimizer and loss function
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# Train the model
num_epochs = 3
model.fit(train_dataset, epochs=num_epochs)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_dataset)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Prepare samples for prediction
sample_texts = [text for _, text in samples]
sample_input_ids = []
sample_attention_masks = []

for text in sample_texts:
    encoded_text = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='tf',
    )
    sample_input_ids.append(encoded_text['input_ids'][0])
    sample_attention_masks.append(encoded_text['attention_mask'][0])

sample_input_ids = np.array(sample_input_ids)
sample_attention_masks = np.array(sample_attention_masks)

# Predict labels for the samples
sample_predictions = model.predict([sample_input_ids, sample_attention_masks])
sample_predicted_labels = np.argmax(sample_predictions, axis=1)

# Print the predicted labels
for i, (label, _) in enumerate(samples):
    predicted_label = sample_predicted_labels[i]
    print(f"Input: {samples[i][1]} | Predicted Label: {predicted_label} ({label})")