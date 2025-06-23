import { useState } from 'react'
import axios from 'axios'
import './PredictionForm.css'

const PredictionForm = () => {
  const initialFormData = {
    Age: 30,
    Years_of_Experience: 5,
    Training_Completion: true,
    Policy_Acknowledgment: true,
    Security_Clearance: true,
    Attendance_Rate: 0.9,
    Performance_Score: 4.0,
    Non_Compliance_Reason: ''
  }

  const [formData, setFormData] = useState(initialFormData)
  const [prediction, setPrediction] = useState(null)
  const [confidence, setConfidence] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showBlockchainOption, setShowBlockchainOption] = useState(false)
  const [blockchainSuccess, setBlockchainSuccess] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    
    // Handle different input types
    const newValue = type === 'checkbox' ? checked : 
                    type === 'number' ? parseFloat(value) : 
                    value
    
    setFormData({
      ...formData,
      [name]: newValue
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)
    setConfidence(null)
    setShowBlockchainOption(false)
    setBlockchainSuccess(false)

    try {
      // Convert boolean values to actual booleans
      const dataToSend = {
        ...formData,
        Training_Completion: Boolean(formData.Training_Completion),
        Policy_Acknowledgment: Boolean(formData.Policy_Acknowledgment),
        Security_Clearance: Boolean(formData.Security_Clearance)
      }

      const response = await axios.post('http://localhost:8000/predict', dataToSend)
      
      setPrediction(response.data.prediction)
      setConfidence(response.data.confidence)
      setShowBlockchainOption(true)
    } catch (err) {
      setError('Error making prediction. Please try again.')
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToBlockchain = async () => {
    setLoading(true)
    setError(null)
    setBlockchainSuccess(false)

    try {
      await axios.post('http://localhost:8000/log-prediction', {
        input_data: formData,
        prediction: prediction
      })
      
      setBlockchainSuccess(true)
      setShowBlockchainOption(false)
    } catch (err) {
      setError('Error adding to blockchain. Please try again.')
      console.error('Blockchain error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFormData(initialFormData)
    setPrediction(null)
    setConfidence(null)
    setError(null)
    setShowBlockchainOption(false)
    setBlockchainSuccess(false)
  }

  return (
    <div className="prediction-container">
      <h2>Employee Compliance Prediction</h2>
      
      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-group">
          <label htmlFor="Age">Age:</label>
          <input
            type="number"
            id="Age"
            name="Age"
            value={formData.Age}
            onChange={handleChange}
            min="18"
            max="70"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="Years_of_Experience">Years of Experience:</label>
          <input
            type="number"
            id="Years_of_Experience"
            name="Years_of_Experience"
            value={formData.Years_of_Experience}
            onChange={handleChange}
            min="0"
            max="50"
            required
          />
        </div>

        <div className="form-group checkbox-group">
          <label htmlFor="Training_Completion">
            <input
              type="checkbox"
              id="Training_Completion"
              name="Training_Completion"
              checked={formData.Training_Completion}
              onChange={handleChange}
            />
            Training Completion
          </label>
        </div>

        <div className="form-group checkbox-group">
          <label htmlFor="Policy_Acknowledgment">
            <input
              type="checkbox"
              id="Policy_Acknowledgment"
              name="Policy_Acknowledgment"
              checked={formData.Policy_Acknowledgment}
              onChange={handleChange}
            />
            Policy Acknowledgment
          </label>
        </div>

        <div className="form-group checkbox-group">
          <label htmlFor="Security_Clearance">
            <input
              type="checkbox"
              id="Security_Clearance"
              name="Security_Clearance"
              checked={formData.Security_Clearance}
              onChange={handleChange}
            />
            Security Clearance
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="Attendance_Rate">Attendance Rate (0.0-1.0):</label>
          <input
            type="number"
            id="Attendance_Rate"
            name="Attendance_Rate"
            value={formData.Attendance_Rate}
            onChange={handleChange}
            min="0"
            max="1"
            step="0.01"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="Performance_Score">Performance Score (1.0-5.0):</label>
          <input
            type="number"
            id="Performance_Score"
            name="Performance_Score"
            value={formData.Performance_Score}
            onChange={handleChange}
            min="1"
            max="5"
            step="0.1"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="Non_Compliance_Reason">Non-Compliance Reason (if any):</label>
          <textarea
            id="Non_Compliance_Reason"
            name="Non_Compliance_Reason"
            value={formData.Non_Compliance_Reason}
            onChange={handleChange}
            rows="3"
          ></textarea>
        </div>

        <div className="form-actions">
          <button type="submit" disabled={loading}>
            {loading ? 'Predicting...' : 'Predict Compliance'}
          </button>
          <button type="button" onClick={handleReset}>
            Reset Form
          </button>
        </div>
      </form>

      {error && <div className="error-message">{error}</div>}

      {prediction && (
        <div className={`prediction-result ${prediction === 'Compliant' ? 'compliant' : 'non-compliant'}`}>
          <h3>Prediction Result:</h3>
          <p className="prediction">{prediction}</p>
          <p className="confidence">Confidence: {(confidence * 100).toFixed(2)}%</p>
        </div>
      )}

      {showBlockchainOption && (
        <div className="blockchain-option">
          <h3>Do you want to add this to blockchain?</h3>
          <div className="blockchain-actions">
            <button onClick={handleAddToBlockchain} disabled={loading}>
              {loading ? 'Adding...' : 'Yes'}
            </button>
            <button onClick={() => setShowBlockchainOption(false)}>No</button>
          </div>
        </div>
      )}

      {blockchainSuccess && (
        <div className="success-message">
          Prediction successfully added to blockchain!
        </div>
      )}
    </div>
  )
}

export default PredictionForm