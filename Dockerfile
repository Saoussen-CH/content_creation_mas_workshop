# Multi-stage build for React frontend + FastAPI backend
# This combines both frontend and backend into a single Cloud Run service

# Stage 1: Build React frontend
FROM node:20-alpine AS frontend-build

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Remove .env files to prevent localhost URLs in production build
RUN rm -f .env .env.local .env.development .env.production

# Build with production config (uses relative URLs via proxy)
RUN npm run build

# Stage 2: Python backend with frontend static files
FROM python:3.11-slim

WORKDIR /app

# Set environment variable to suppress debconf warnings
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/api_server.py ./

# Copy built frontend from previous stage
COPY --from=frontend-build /frontend/dist ./static

# Expose port (Cloud Run uses PORT environment variable)
ENV PORT=8080
EXPOSE 8080

# Run the application with uvicorn
# Cloud Run will set PORT=8080 by default
CMD exec uvicorn api_server:app --host 0.0.0.0 --port ${PORT}
