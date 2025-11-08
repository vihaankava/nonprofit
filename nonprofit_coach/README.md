# Nonprofit Idea Coach

A web application that helps individuals transform their cause-based ideas into actionable nonprofit initiatives.

## Setup

1. Install Python 3.8 or higher

2. Navigate to the nonprofit_coach directory:
```bash
cd nonprofit_coach
```

3. Create and activate a virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (optional):
```bash
cp .env.example .env
```

6. Run the application:
```bash
python app.py
```

7. Open your browser to `http://localhost:5001`

8. Enter your Claude API key to get started

## Note on Virtual Environments

If you see an "externally managed environment" error, you need to use a virtual environment (step 3 above). This is required on newer versions of Python/macOS.

To deactivate the virtual environment when you're done:
```bash
deactivate
```

## Features

- Guided idea development questionnaire
- AI-assisted content generation
- Personalized website generation with:
  - Marketing tools
  - Team building resources
  - Funding guidance
  - Implementation research

## Requirements

- Python 3.8+
- Flask
- Anthropic Claude API key
