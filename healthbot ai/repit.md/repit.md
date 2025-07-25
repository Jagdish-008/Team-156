# SwasthyaBot Healthcare Assistant

## Overview

SwasthyaBot is a bilingual healthcare assistant designed to serve rural India. The application provides symptom analysis, health guidance, and helps users find nearby medical facilities. It operates both as a web application and a Telegram bot, supporting English and Hindi languages to ensure accessibility for diverse populations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular Flask-based architecture with distinct components for different functionalities:

- **Web Interface**: Flask application serving an interactive chat interface
- **Telegram Bot**: Integration with Telegram Bot API for mobile access
- **Diagnosis Engine**: Rule-based symptom analysis system
- **Translation Manager**: Bilingual support for English and Hindi
- **Static Data Storage**: JSON files for symptoms rules and hospital information

## Key Components

### 1. Flask Web Application (`app.py`, `main.py`)
- **Purpose**: Provides the main web interface for user interactions
- **Key Features**: Session management, chat endpoint, conversation state tracking
- **Architecture**: RESTful API design with JSON responses
- **Session Management**: Server-side session storage for conversation continuity

### 2. Telegram Bot Integration (`bot.py`)
- **Purpose**: Extends accessibility through Telegram messaging platform
- **Key Features**: Webhook processing, user state management, command handling
- **Architecture**: Event-driven message processing with state persistence
- **User State**: In-memory storage of conversation states per chat ID

### 3. Diagnosis Engine (`diagnosis.py`)
- **Purpose**: Core medical logic for symptom analysis and advice generation
- **Approach**: Rule-based system using keyword matching and predefined conditions
- **Data Sources**: JSON-based symptom rules and hospital directory
- **Fallback**: Default data structures when external files are unavailable

### 4. Translation Manager (`translations.py`)
- **Purpose**: Provides bilingual support for UI and medical content
- **Languages**: English and Hindi
- **Scope**: User interface elements, medical advice, and system messages

### 5. Frontend Interface
- **Technology**: Bootstrap-based responsive design with custom CSS
- **Features**: Dark theme, chat interface, language switching, emergency alerts
- **JavaScript**: Real-time chat functionality with message state management

## Data Flow

### 1. Conversation Flow
```
User Input → Language Detection → State Management → Symptom Analysis → Response Generation → Translation → Output
```

### 2. Web Chat Flow
1. User sends message via web interface
2. Flask receives POST request to `/chat` endpoint
3. Session state retrieved/initialized
4. Message processed through diagnosis engine
5. Response generated and translated
6. JSON response sent back to frontend
7. Session state updated

### 3. Telegram Bot Flow
1. Telegram sends webhook update
2. Bot processes message and extracts user context
3. User state retrieved from in-memory storage
4. Message processed through shared diagnosis logic
5. Response sent via Telegram Bot API
6. User state updated

## External Dependencies

### Required Services
- **Telegram Bot API**: For mobile messaging functionality
- **Environment Variables**: 
  - `TELEGRAM_BOT_TOKEN`: Bot authentication
  - `SESSION_SECRET`: Flask session security

### Frontend Dependencies
- **Bootstrap**: UI framework via CDN
- **Feather Icons**: Icon library
- **Custom CSS**: Application-specific styling

### Data Dependencies
- **Static JSON Files**: 
  - `data/symptoms_rules.json`: Medical condition definitions
  - `data/hospitals.json`: Healthcare facility directory
  - `data/translations.json`: Bilingual text content

## Deployment Strategy

### Current Setup
- **Runtime**: Python Flask application
- **Port**: 5000 (configurable)
- **Host**: 0.0.0.0 for external access
- **Environment**: Development mode with debug enabled

### Production Considerations
- **Scaling**: Stateless design enables horizontal scaling
- **Session Storage**: Consider Redis or database for production
- **Security**: Environment variable management for sensitive tokens
- **Monitoring**: Logging configured for debugging and error tracking

### Database Integration Readiness
- **Current State**: File-based JSON storage
- **Migration Path**: Diagnosis engine designed for easy database integration
- **Recommended**: PostgreSQL for structured medical data and user sessions
- **Schema Needs**: User sessions, medical conditions, hospital data, conversation logs

The application architecture prioritizes simplicity and accessibility while maintaining the flexibility to scale and integrate additional healthcare data sources as needed.