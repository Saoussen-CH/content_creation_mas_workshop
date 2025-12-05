import React, { useState } from 'react'

function ContentDisplay({ content }) {
  const [activeTab, setActiveTab] = useState('preview')

  const copyToClipboard = () => {
    navigator.clipboard.writeText(content)
    alert('Content copied to clipboard!')
  }

  const downloadContent = () => {
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'content-package.md'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="content-display">
      <div className="content-header">
        <h2>✅ Generated Content Package</h2>
        <div className="content-actions">
          <button onClick={copyToClipboard} className="action-button">
            📋 Copy
          </button>
          <button onClick={downloadContent} className="action-button">
            💾 Download
          </button>
        </div>
      </div>

      <div className="content-tabs">
        <button
          className={`tab ${activeTab === 'preview' ? 'active' : ''}`}
          onClick={() => setActiveTab('preview')}
        >
          👁️ Preview
        </button>
        <button
          className={`tab ${activeTab === 'markdown' ? 'active' : ''}`}
          onClick={() => setActiveTab('markdown')}
        >
          📝 Markdown
        </button>
      </div>

      <div className="content-body">
        {activeTab === 'preview' ? (
          <div className="content-preview">
            <MarkdownRenderer content={content} />
          </div>
        ) : (
          <pre className="content-markdown">
            <code>{content}</code>
          </pre>
        )}
      </div>
    </div>
  )
}

// Simple markdown renderer component
function MarkdownRenderer({ content }) {
  // Basic markdown to HTML conversion
  const renderMarkdown = (text) => {
    if (!text) return ''

    // Headers
    text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>')
    text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>')
    text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>')

    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

    // Italic
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>')

    // Line breaks
    text = text.replace(/\n/g, '<br />')

    // Lists
    text = text.replace(/^\* (.*$)/gim, '<li>$1</li>')
    text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')

    return text
  }

  return (
    <div
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
    />
  )
}

export default ContentDisplay
