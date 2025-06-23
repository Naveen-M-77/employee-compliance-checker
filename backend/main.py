import os
import json
import pickle
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from tensorflow.keras.preprocessing.sequence import pad_sequences
from blockchain import Blockchain

app = FastAPI(title="Employee Compliance Prediction API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize blockchain
blockchain = Blockchain(blockchain_file="D:/Dev/employee-compliance-trae/backend/blockchain.json")

# Load model artifacts
MODEL_DIR = "D:/Dev/employee-compliance-trae/model/artifacts"

# Load the model
model = tf.keras.models.load_model(os.path.join(MODEL_DIR, "model.h5"))

# Load the tokenizer
with open(os.path.join(MODEL_DIR, "tokenizer.json"), 'r') as f:
    tokenizer_json = f.read()
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)

# Load the scaler
with open(os.path.join(MODEL_DIR, "scaler.pkl"), 'rb') as f:
    scaler = pickle.load(f)

# Load feature configuration
with open(os.path.join(MODEL_DIR, "feature_config.json"), 'r') as f:
    feature_config = json.load(f)

numerical_features = feature_config["numerical_features"]
boolean_features = feature_config["boolean_features"]
max_sequence_length = feature_config["max_sequence_length"]

# Define input model
class EmployeeData(BaseModel):
    Age: int
    Years_of_Experience: int
    Training_Completion: bool
    Policy_Acknowledgment: bool
    Security_Clearance: bool
    Attendance_Rate: float
    Performance_Score: float
    Non_Compliance_Reason: Optional[str] = None

# Define prediction result model
class PredictionResult(BaseModel):
    prediction: str
    confidence: float

# Define blockchain log model
class BlockchainLog(BaseModel):
    input_data: Dict[str, Any]
    prediction: str

@app.get("/")
def read_root():
    return {"message": "Employee Compliance Prediction API"}

@app.post("/predict", response_model=PredictionResult)
def predict(employee_data: EmployeeData):
    try:
        # Process numerical features
        numerical_data = np.array([
            employee_data.Age,
            employee_data.Years_of_Experience,
            employee_data.Attendance_Rate,
            employee_data.Performance_Score
        ]).reshape(1, -1)
        
        # Scale numerical features
        numerical_data_scaled = scaler.transform(numerical_data)
        
        # Process boolean features
        boolean_data = np.array([
            int(employee_data.Training_Completion),
            int(employee_data.Policy_Acknowledgment),
            int(employee_data.Security_Clearance)
        ]).reshape(1, -1)
        
        # Process text data
        text = employee_data.Non_Compliance_Reason if employee_data.Non_Compliance_Reason else ""
        text_seq = tokenizer.texts_to_sequences([text])
        text_padded = pad_sequences(text_seq, maxlen=max_sequence_length, padding='post')
        
        # Make prediction
        prediction_prob = model.predict([numerical_data_scaled, boolean_data, text_padded])[0][0]
        
        # Convert probability to class
        prediction_class = "Compliant" if prediction_prob >= 0.5 else "Non-Compliant"
        confidence = float(prediction_prob if prediction_prob >= 0.5 else 1 - prediction_prob)
        
        return PredictionResult(prediction=prediction_class, confidence=confidence)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/log-prediction")
def log_prediction(log_data: BlockchainLog):
    try:
        # Add prediction to blockchain
        block = blockchain.add_block(log_data.input_data, log_data.prediction)
        return {"message": "Prediction logged to blockchain", "block": block.to_dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

@app.get("/chain")
def get_chain():
    try:
        chain = blockchain.get_chain()
        return {"chain": chain, "length": len(chain)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)