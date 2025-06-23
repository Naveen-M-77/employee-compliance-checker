import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json
import os

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Load the dataset
df = pd.read_csv('D:\\Dev\\employee-compliance-trae\\model\\employee_compliance_dataset.csv')

# Separate features and target
X = df.drop(['Compliance_Status', 'Employee_ID'], axis=1)
y = df['Compliance_Status']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Process text data (Non_Compliance_Reason)
max_words = 100
max_sequence_length = 20

# Initialize and fit the tokenizer on the text data
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
# Filter out NaN values before fitting
non_compliance_reasons = X_train['Non_Compliance_Reason'].fillna('').astype(str).values
tokenizer.fit_on_texts(non_compliance_reasons)

# Convert text to sequences
X_train_text_seq = tokenizer.texts_to_sequences(X_train['Non_Compliance_Reason'].fillna('').astype(str))
X_test_text_seq = tokenizer.texts_to_sequences(X_test['Non_Compliance_Reason'].fillna('').astype(str))

# Pad sequences to ensure uniform length
X_train_text_padded = pad_sequences(X_train_text_seq, maxlen=max_sequence_length, padding='post')
X_test_text_padded = pad_sequences(X_test_text_seq, maxlen=max_sequence_length, padding='post')

# Process numerical features
numerical_features = ['Age', 'Years_of_Experience', 'Attendance_Rate', 'Performance_Score']
X_train_numerical = X_train[numerical_features].values
X_test_numerical = X_test[numerical_features].values

# Standardize numerical features
scaler = StandardScaler()
X_train_numerical_scaled = scaler.fit_transform(X_train_numerical)
X_test_numerical_scaled = scaler.transform(X_test_numerical)

# Process boolean features
boolean_features = ['Training_Completion', 'Policy_Acknowledgment', 'Security_Clearance']
X_train_boolean = X_train[boolean_features].values
X_test_boolean = X_test[boolean_features].values

# Build the model
# Input layers
numerical_input = keras.Input(shape=(len(numerical_features),), name='numerical_input')
boolean_input = keras.Input(shape=(len(boolean_features),), name='boolean_input')
text_input = keras.Input(shape=(max_sequence_length,), name='text_input')

# Numerical features branch
x_numerical = layers.Dense(16, activation='relu')(numerical_input)
x_numerical = layers.Dense(8, activation='relu')(x_numerical)

# Boolean features branch
x_boolean = layers.Dense(8, activation='relu')(boolean_input)
x_boolean = layers.Dense(4, activation='relu')(x_boolean)

# Text features branch
x_text = layers.Embedding(input_dim=max_words, output_dim=16, input_length=max_sequence_length)(text_input)
x_text = layers.GlobalAveragePooling1D()(x_text)
x_text = layers.Dense(8, activation='relu')(x_text)

# Combine all features
combined = layers.concatenate([x_numerical, x_boolean, x_text])

# Output layer
output = layers.Dense(16, activation='relu')(combined)
output = layers.Dense(8, activation='relu')(output)
output = layers.Dense(1, activation='sigmoid')(output)

# Create the model
model = keras.Model(
    inputs=[numerical_input, boolean_input, text_input],
    outputs=output
)

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    [X_train_numerical_scaled, X_train_boolean, X_train_text_padded],
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(
    [X_test_numerical_scaled, X_test_boolean, X_test_text_padded],
    y_test,
    verbose=1
)

print(f"Test accuracy: {test_accuracy:.4f}")

# Save model artifacts
artifacts_dir = 'D:\\Dev\\employee-compliance-trae\\model\\artifacts'
if not os.path.exists(artifacts_dir):
    os.makedirs(artifacts_dir)

# Save the model
model.save(os.path.join(artifacts_dir, 'model.h5'))

# Save the tokenizer
tokenizer_json = tokenizer.to_json()
with open(os.path.join(artifacts_dir, 'tokenizer.json'), 'w') as f:
    f.write(tokenizer_json)

# Save the scaler
with open(os.path.join(artifacts_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

# Save feature names for reference
feature_config = {
    'numerical_features': numerical_features,
    'boolean_features': boolean_features,
    'max_sequence_length': max_sequence_length,
    'max_words': max_words
}

with open(os.path.join(artifacts_dir, 'feature_config.json'), 'w') as f:
    json.dump(feature_config, f)

print("Model training completed and artifacts saved.")