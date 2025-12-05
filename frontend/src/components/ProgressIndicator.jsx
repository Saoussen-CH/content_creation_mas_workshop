import React from 'react'

function ProgressIndicator({ progress, isGenerating }) {
  return (
    <div className="progress-indicator">
      <h3>🔄 Workflow Progress</h3>

      <div className="progress-timeline">
        {progress.map((item, index) => (
          <div key={index} className={`progress-item ${item.type}`}>
            {item.type === 'info' && (
              <div className="progress-message">
                <span className="icon">ℹ️</span>
                <span>{item.message}</span>
              </div>
            )}

            {item.type === 'event' && (
              <div className="progress-event">
                <span className="icon">🤖</span>
                <div className="event-details">
                  <strong>{item.author}</strong>
                  {item.preview && (
                    <p className="event-preview">{item.preview}...</p>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {isGenerating && (
          <div className="progress-item active">
            <div className="progress-message">
              <span className="spinner-small"></span>
              <span>Processing...</span>
            </div>
          </div>
        )}
      </div>

      <div className="progress-stages">
        <div className="stage">
          <div className="stage-icon">📥</div>
          <div className="stage-name">Intake</div>
        </div>
        <div className="stage-arrow">→</div>
        <div className="stage">
          <div className="stage-icon">🔍</div>
          <div className="stage-name">Research</div>
        </div>
        <div className="stage-arrow">→</div>
        <div className="stage">
          <div className="stage-icon">✍️</div>
          <div className="stage-name">Draft</div>
        </div>
        <div className="stage-arrow">→</div>
        <div className="stage">
          <div className="stage-icon">✅</div>
          <div className="stage-name">Quality Check</div>
        </div>
        <div className="stage-arrow">→</div>
        <div className="stage">
          <div className="stage-icon">🚀</div>
          <div className="stage-name">Multi-Channel</div>
        </div>
        <div className="stage-arrow">→</div>
        <div className="stage">
          <div className="stage-icon">📦</div>
          <div className="stage-name">Package</div>
        </div>
      </div>
    </div>
  )
}

export default ProgressIndicator
