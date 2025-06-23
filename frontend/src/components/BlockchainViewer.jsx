import { useState, useEffect } from 'react'
import axios from 'axios'
import './BlockchainViewer.css'

const BlockchainViewer = () => {
  const [blockchain, setBlockchain] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedBlocks, setExpandedBlocks] = useState({})

  useEffect(() => {
    fetchBlockchain()
  }, [])

  const fetchBlockchain = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await axios.get('http://localhost:8000/chain')
      setBlockchain(response.data.chain)
    } catch (err) {
      setError('Error fetching blockchain data. Please try again.')
      console.error('Blockchain fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  const toggleBlockExpansion = (index) => {
    setExpandedBlocks(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  if (loading) {
    return <div className="loading">Loading blockchain data...</div>
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={fetchBlockchain}>Try Again</button>
      </div>
    )
  }

  return (
    <div className="blockchain-container">
      <h2>Blockchain Ledger</h2>
      <p className="blockchain-info">
        Total Blocks: {blockchain.length}
      </p>
      <button onClick={fetchBlockchain} className="refresh-button">
        Refresh Blockchain
      </button>

      <div className="blockchain-list">
        {blockchain.map((block, index) => (
          <div 
            key={block.hash} 
            className={`blockchain-block ${expandedBlocks[index] ? 'expanded' : ''}`}
          >
            <div className="block-header" onClick={() => toggleBlockExpansion(index)}>
              <h3>Block #{block.index}</h3>
              <span className="expand-icon">{expandedBlocks[index] ? '▼' : '►'}</span>
            </div>
            
            {expandedBlocks[index] && (
              <div className="block-details">
                <div className="block-info">
                  <p><strong>Timestamp:</strong> {formatTimestamp(block.timestamp)}</p>
                  <p><strong>Hash:</strong> <span className="hash">{block.hash}</span></p>
                  <p><strong>Previous Hash:</strong> <span className="hash">{block.previous_hash}</span></p>
                  <p><strong>Prediction:</strong> <span className={`prediction ${block.prediction === 'Compliant' ? 'compliant' : block.prediction === 'Non-Compliant' ? 'non-compliant' : ''}`}>
                    {block.prediction}
                  </span></p>
                </div>
                
                {block.index > 0 && (
                  <div className="block-data">
                    <h4>Input Data:</h4>
                    <div className="data-table">
                      <table>
                        <tbody>
                          {Object.entries(block.data).map(([key, value]) => (
                            <tr key={key}>
                              <td>{key.replace(/_/g, ' ')}</td>
                              <td>
                                {typeof value === 'boolean' 
                                  ? value ? 'Yes' : 'No'
                                  : value}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default BlockchainViewer