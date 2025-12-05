import React, { useState } from 'react'
import ContentForm from './components/ContentForm'
import ContentDisplay from './components/ContentDisplay'
import ProgressIndicator from './components/ProgressIndicator'
import TextAnalyzer from './components/TextAnalyzer'
import './styles/App.css'

function App() {
  const [activeTab, setActiveTab] = useState('create')
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState([])
  const [generatedContent, setGeneratedContent] = useState(null)
  const [error, setError] = useState(null)

  const handleContentGeneration = (formData) => {
    setIsGenerating(true)
    setProgress([])
    setGeneratedContent(null)
    setError(null)

    // Use relative URL - works both in development (via Vite proxy) and production (same server)
    const apiUrl = '/api/create-content'

    // Use fetch with streaming for POST requests
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        topic: formData.topic,
        target_audience: formData.targetAudience,
        tone: formData.tone,
        keywords: formData.keywords,
      }),
    })
      .then(response => {
        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        const readStream = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              setIsGenerating(false)
              return
            }

            const chunk = decoder.decode(value)
            const lines = chunk.split('\n')

            lines.forEach(line => {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.substring(6))

                  if (data.type === 'status') {
                    setProgress(prev => [...prev, { type: 'info', message: data.message }])
                  } else if (data.type === 'event') {
                    setProgress(prev => [...prev, {
                      type: 'event',
                      author: data.author,
                      preview: data.content_preview
                    }])
                  } else if (data.type === 'complete') {
                    setGeneratedContent(data.content)
                    setIsGenerating(false)
                  } else if (data.type === 'error') {
                    setError(data.message)
                    setIsGenerating(false)
                  }
                } catch (e) {
                  console.error('Error parsing SSE data:', e)
                }
              }
            })

            readStream()
          })
        }

        readStream()
      })
      .catch(err => {
        setError(err.message)
        setIsGenerating(false)
      })
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎨 Content Creation Studio</h1>
        <p>AI-Powered Multi-Agent Content Generation</p>
      </header>

      <main className="app-main">
        <div className="main-tabs">
          <button
            className={`main-tab ${activeTab === 'create' ? 'active' : ''}`}
            onClick={() => setActiveTab('create')}
          >
            🚀 Create Content
          </button>
          <button
            className={`main-tab ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            📊 Analyze Text
          </button>
        </div>

        <div className="content-container">
          {activeTab === 'create' && (
            <>
              <div className="form-section">
                <ContentForm
                  onSubmit={handleContentGeneration}
                  isGenerating={isGenerating}
                />
              </div>

          {(isGenerating || progress.length > 0) && (
            <div className="progress-section">
              <ProgressIndicator
                progress={progress}
                isGenerating={isGenerating}
              />
            </div>
          )}

          {error && (
            <div className="error-section">
              <div className="error-message">
                <strong>Error:</strong> {error}
              </div>
            </div>
          )}

              {generatedContent && (
                <div className="content-section">
                  <ContentDisplay content={generatedContent} />
                </div>
              )}
            </>
          )}

          {activeTab === 'analyze' && (
            <div className="form-section">
              <TextAnalyzer />
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Powered by Google ADK & Gemini AI</p>
      </footer>
    </div>
  )
}

export default App
