# Employee Compliance Prediction System

A full-stack application that predicts employee compliance using deep learning. The system includes a React frontend, FastAPI backend, and a simple blockchain implementation for logging predictions.

## Project Structure

```
├── model/               # Deep learning model and training
│   ├── artifacts/       # Saved model artifacts
│   ├── employee_compliance_dataset.csv
│   └── train_model.py   # Model training script
├── backend/             # FastAPI backend
│   ├── blockchain.py    # Blockchain implementation
│   ├── main.py          # FastAPI application
│   └── requirements.txt # Backend dependencies
└── frontend/            # React frontend
    ├── public/          # Static assets
    ├── src/             # React source code
    ├── index.html       # HTML entry point
    ├── package.json     # Frontend dependencies
    └── vite.config.js   # Vite configuration
```

## Features

- **Deep Learning Model**: Predicts employee compliance based on various factors
- **FastAPI Backend**: Provides prediction endpoints and blockchain functionality
- **React Frontend**: User-friendly interface for making predictions and viewing blockchain
- **Blockchain**: Simple implementation for immutable logging of predictions

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

3. Start the development server:
   ```
   npm run dev
   ```
   or
   ```
   yarn dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## API Endpoints

- `POST /predict`: Predicts employee compliance based on input data
- `POST /log-prediction`: Logs a prediction to the blockchain
- `GET /chain`: Returns the full blockchain

## Model Training

To train the model from scratch:

1. Navigate to the model directory:
   ```
   cd model
   ```

2. Run the training script:
   ```
   python train_model.py
   ```

This will generate model artifacts in the `model/artifacts` directory.

## Technologies Used

- **Frontend**: React, Vite, Axios
- **Backend**: FastAPI, TensorFlow/Keras
- **Data Storage**: Simple blockchain implementation
- **Machine Learning**: Deep learning with TensorFlow/Keras