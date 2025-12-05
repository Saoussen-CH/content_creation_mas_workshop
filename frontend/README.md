# Content Creation Studio - Frontend

React-based frontend for the AI-powered multi-agent content creation system.

## Features

- 📝 Interactive content brief form
- 🔄 Real-time workflow progress tracking
- ✨ Live content generation with SSE (Server-Sent Events)
- 📊 Multi-agent execution visualization
- 💾 Download generated content as Markdown
- 📋 Copy to clipboard functionality
- 🎨 Modern, responsive UI

## Setup

### Prerequisites

- Node.js 18+ and npm
- Backend API server running on http://localhost:8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at http://localhost:3000

### Build

```bash
npm run build
```

## Architecture

### Components

- **App.jsx** - Main application component with state management
- **ContentForm.jsx** - Form for content brief input
- **ContentDisplay.jsx** - Display generated content with preview/markdown tabs
- **ProgressIndicator.jsx** - Real-time workflow progress visualization

### API Integration

The frontend communicates with the FastAPI backend using:
- **Fetch API** with streaming for real-time content generation
- **Server-Sent Events (SSE)** for progress updates
- **REST endpoints** for text analysis and publishing

## Usage

1. Fill in the content brief form:
   - Topic
   - Target Audience
   - Tone
   - SEO Keywords

2. Click "Generate Content Package"

3. Watch the multi-agent workflow in real-time:
   - Intake → Research → Draft → Quality Check → Multi-Channel → Package

4. View the generated content in Preview or Markdown mode

5. Copy to clipboard or download as .md file

## Workflow Stages

1. **📥 Intake** - Parse content brief and extract parameters
2. **🔍 Research** - Find trending topics and angles
3. **✍️ Draft** - Create initial content draft
4. **✅ Quality Check** - Evaluate and improve content quality
5. **🚀 Multi-Channel** - Generate blog, social, email, and SEO content
6. **📦 Package** - Assemble final deliverable

## Tech Stack

- React 18
- Vite (build tool)
- Axios (HTTP client)
- CSS3 with CSS Variables
- Server-Sent Events (SSE)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
