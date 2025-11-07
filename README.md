# Nonprofit Idea Coach

A web application that guides individuals through the process of transforming their cause-based ideas into actionable nonprofit initiatives. The system provides structured coaching through idea development and creates personalized websites with AI-assisted tools for marketing, team building, funding, and research.

## Project Structure

```
nonprofit-idea-coach/
├── frontend/          # React.js frontend application
├── backend/           # Node.js Express API server
├── shared/            # Shared TypeScript types and interfaces
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (>= 18.0.0)
- npm (>= 8.0.0)
- PostgreSQL database

### Installation

1. Clone the repository
2. Install dependencies for all packages:
   ```bash
   npm run install:all
   ```

3. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

### Development

Start both frontend and backend in development mode:
```bash
npm run dev
```

Or start them individually:
```bash
# Frontend (runs on http://localhost:3000)
npm run dev:frontend

# Backend (runs on http://localhost:3001)
npm run dev:backend
```

### Building

Build both applications:
```bash
npm run build
```

### Testing

Run tests for both applications:
```bash
npm test
```

## Architecture

The application follows a monorepo structure with three main packages:

- **Frontend**: React.js application with TypeScript
- **Backend**: Node.js Express API with TypeScript
- **Shared**: Common TypeScript interfaces and types

## Features

1. **Idea Development Session**: Structured questionnaire to refine nonprofit concepts
2. **AI Content Generation**: Marketing, team building, funding, and research content
3. **Website Generator**: Personalized websites for each nonprofit idea
4. **User Management**: Authentication and user profiles