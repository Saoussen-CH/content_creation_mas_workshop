import React, { useState } from 'react'

function ContentForm({ onSubmit, isGenerating }) {
  const [formData, setFormData] = useState({
    topic: '',
    targetAudience: '',
    tone: '',
    keywords: '',
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const isFormValid = formData.topic && formData.targetAudience && formData.tone && formData.keywords

  return (
    <form className="content-form" onSubmit={handleSubmit}>
      <h2>📝 Content Brief</h2>

      <div className="form-group">
        <label htmlFor="topic">Topic *</label>
        <input
          type="text"
          id="topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          placeholder="e.g., Productivity hacks using AI for remote workers"
          required
          disabled={isGenerating}
        />
      </div>

      <div className="form-group">
        <label htmlFor="targetAudience">Target Audience *</label>
        <input
          type="text"
          id="targetAudience"
          name="targetAudience"
          value={formData.targetAudience}
          onChange={handleChange}
          placeholder="e.g., Remote professionals and digital nomads"
          required
          disabled={isGenerating}
        />
      </div>

      <div className="form-group">
        <label htmlFor="tone">Tone *</label>
        <select
          id="tone"
          name="tone"
          value={formData.tone}
          onChange={handleChange}
          required
          disabled={isGenerating}
        >
          <option value="">Select a tone...</option>
          <option value="Professional">Professional</option>
          <option value="Conversational">Conversational</option>
          <option value="Friendly">Friendly</option>
          <option value="Casual">Casual</option>
          <option value="Formal">Formal</option>
          <option value="Educational">Educational</option>
          <option value="Enthusiastic">Enthusiastic</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="keywords">SEO Keywords *</label>
        <input
          type="text"
          id="keywords"
          name="keywords"
          value={formData.keywords}
          onChange={handleChange}
          placeholder="e.g., AI productivity, remote work, automation tools"
          required
          disabled={isGenerating}
        />
        <small>Comma-separated keywords</small>
      </div>

      <button
        type="submit"
        className="submit-button"
        disabled={!isFormValid || isGenerating}
      >
        {isGenerating ? (
          <>
            <span className="spinner"></span>
            Generating Content...
          </>
        ) : (
          <>
            🚀 Generate Content Package
          </>
        )}
      </button>
    </form>
  )
}

export default ContentForm
