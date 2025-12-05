import React, { useState } from 'react'

function TextAnalyzer() {
  const [text, setText] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setIsAnalyzing(true)
    setError(null)
    setAnalysis(null)

    try {
      // Use relative URL - works both in development (via Vite proxy) and production (same server)
      const response = await fetch('/api/analyze-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setAnalysis(data.analysis)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="text-analyzer">
      <h2>📊 Text Analysis</h2>
      <p className="subtitle">Analyze text for word count, readability, and hashtags</p>

      <form onSubmit={handleAnalyze}>
        <div className="form-group">
          <label htmlFor="text">Text to Analyze *</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your text here for analysis..."
            rows={8}
            required
            disabled={isAnalyzing}
          />
          <small>{text.length} characters</small>
        </div>

        <button
          type="submit"
          className="submit-button"
          disabled={!text.trim() || isAnalyzing}
        >
          {isAnalyzing ? (
            <>
              <span className="spinner"></span>
              Analyzing...
            </>
          ) : (
            '🔍 Analyze Text'
          )}
        </button>
      </form>

      {error && (
        <div className="error-message" style={{ marginTop: '1rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {analysis && (
        <div className="analysis-results">
          <h3>✅ Analysis Results</h3>
          <div className="analysis-content">
            <pre>{analysis}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default TextAnalyzer
