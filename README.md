# Nonprofit Idea Coach

An AI-powered tool that helps you develop nonprofit ideas into actionable startup plans with personalized websites.

## Features

- 🤖 AI-guided questionnaire to develop your nonprofit idea
- 🎨 Automatically generated personalized website for each nonprofit
- 🔍 **Web search integration** for real-time research (grants, organizations, resources)
- 📚 Research & Planning tools (implementation steps, local orgs, resources)
- 👥 Team Building tools (recruiting pitch, job descriptions, volunteer forms)
- 💰 Funding Strategy tools (grant proposals, donor letters, budget plans)
- 📢 Marketing Materials (emails, flyers, social media posts)
- 💬 AI chat assistant for each section
- 🗑️ Easy idea management with delete functionality
- ⚡ Smart caching for improved performance

## Quick Start

### One-Command Installation

**macOS/Linux:**
```bash
git clone https://github.com/vihaankava/nonprofit.git && cd nonprofit/nonprofit_coach && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && echo "✅ Setup complete! Edit .env with your API key, then run: python app.py"
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/vihaankava/nonprofit.git; cd nonprofit/nonprofit_coach; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt; copy .env.example .env; Write-Host "✅ Setup complete! Edit .env with your API key, then run: python app.py"
```

**Windows (Command Prompt):**
```cmd
git clone https://github.com/vihaankava/nonprofit.git && cd nonprofit\nonprofit_coach && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && copy .env.example .env && echo Setup complete! Edit .env with your API key, then run: python app.py
```

Then:
1. Edit `.env` and add your [Anthropic API key](https://console.anthropic.com/)
2. Run: `python app.py`
3. Open: http://localhost:5001

### Detailed Setup Guides

- **Windows:** See [SETUP_WINDOWS.md](SETUP_WINDOWS.md)
- **Linux:** See [SETUP_LINUX.md](SETUP_LINUX.md)
- **Chromebook:** See [SETUP_CHROMEBOOK.md](SETUP_CHROMEBOOK.md)
- **macOS:** Follow instructions below

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Download the code:**
   ```bash
   git clone https://github.com/vihaankava/Coaching-for-non-Profits.git
   cd Coaching-for-non-Profits
   ```

2. **Navigate to the nonprofit_coach directory:**
   ```bash
   cd nonprofit_coach
   ```

3. **Create and activate a virtual environment:**
   
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

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install flask anthropic python-dotenv requests
   ```

5. **Set up your API keys:**
   
   Open the `.env` file and add your API keys:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   SECRET_KEY=your-secret-key-change-in-production
   
   # Optional: Enable web search (recommended)
   SEARCH_ENABLED=true
   SEARCH_PROVIDER=brave
   BRAVE_API_KEY=your-brave-api-key-here
   ```
   
   To get a Brave Search API key (free tier available):
   - Visit [Brave Search API](https://brave.com/search/api/)
   - Sign up for an account
   - Get your API key from the dashboard

6. **Run the application:**
   ```bash
   python app.py
   ```
   
   Note: Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt)

7. **Open your browser:**
   
   Go to: `http://127.0.0.1:5001`

## How to Use

### Creating a New Nonprofit Idea

1. Click on the "New Idea" tab
2. (Optional) Enter your Anthropic API key, or leave blank to use the one from `.env`
3. Click "Start Questionnaire"
4. Answer 7 questions about your nonprofit idea
5. Click "Generate Website"
6. Your personalized nonprofit website will be created!

### Using Your Generated Website

After creating an idea, click on it from the "All Ideas" tab. You'll see:

- **Home Page**: Overview of your nonprofit
- **Research Section**: Get implementation steps, find local organizations, discover resources
- **Team Section**: Create recruiting materials, job descriptions, volunteer forms
- **Funding Section**: Generate grant proposals, donor letters, budget plans
- **Marketing Section**: Create emails, flyers, social media posts

Each section has:
- Buttons to generate specific content
- AI chat assistant to refine content or ask questions

### Managing Ideas

- **View all ideas**: Click the "All Ideas" tab
- **Delete an idea**: Hover over an idea card and click the red × button

## Project Structure

```
nonprofit_coach/
├── app.py                 # Main Flask application
├── db.py                  # Database functions
├── ai_service.py          # AI/Claude integration
├── site_generator.py      # Website generation logic
├── search_service.py      # Web search orchestration
├── search_cache.py        # Search result caching
├── search_config.py       # Search configuration & validation
├── search_providers/      # Search provider implementations
│   ├── base.py           # Abstract provider interface
│   └── brave.py          # Brave Search provider (coming soon)
├── templates/             # HTML templates
│   ├── index.html
│   ├── generated_home.html
│   ├── generated_section.html
│   └── generated_base.html
├── static/                # CSS and JavaScript
│   ├── style.css
│   └── app.js
├── nonprofit.db           # SQLite database (created automatically)
└── generated_sites/       # Generated websites (created automatically)
```

## Database Schema

The application uses SQLite with three tables:

- **ideas**: Stores nonprofit ideas and questionnaire responses
- **content**: Stores generated content for each section
- **volunteers**: Stores volunteer information (optional feature)

## API Endpoints

- `POST /api/setup` - Configure API key
- `POST /api/question` - Get AI follow-up questions
- `POST /api/complete` - Complete questionnaire and generate site
- `POST /api/generate` - Generate section content
- `POST /api/chat` - Chat with AI assistant
- `DELETE /api/ideas/<id>` - Delete an idea
- `GET /site/<id>` - View generated site home page
- `GET /site/<id>/<section>` - View section page

## Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **AI**: Anthropic Claude (Haiku model)
- **Search**: Brave Search API (optional)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Caching**: In-memory TTL-based cache

## Development

### Running in Development Mode

The app runs in debug mode by default on port 5001:

```bash
python3 app.py
```

### Creating a Backup

The project includes git tags for version control:

```bash
# View available tags
git tag

# Checkout a specific version
git checkout v1.1-working
```

## Search Integration (Optional)

The app includes web search capabilities to enhance content generation with real-time data about grants, local organizations, and resources.

### Configuration

Search is configured via environment variables in `.env`:

```bash
# Enable/disable search
SEARCH_ENABLED=true

# Choose provider (brave, google, bing)
SEARCH_PROVIDER=brave

# Provider API keys
BRAVE_API_KEY=your_brave_api_key_here
GOOGLE_SEARCH_API_KEY=
GOOGLE_SEARCH_ENGINE_ID=
BING_SEARCH_API_KEY=

# Cache settings
SEARCH_CACHE_TTL=86400        # 24 hours
SEARCH_CACHE_MAX_SIZE=1000    # Max cached queries

# Search behavior
SEARCH_TIMEOUT=5              # Seconds
SEARCH_MAX_RESULTS=10
SEARCH_RETRY_ATTEMPTS=1
```

### Supported Providers

- **Brave Search** (recommended): Free tier available, no credit card required
- **Google Custom Search**: Requires API key and Custom Search Engine ID
- **Bing Search**: Requires Azure subscription

The app will work without search enabled, but won't include real-time web data in generated content.

## Troubleshooting

### "Externally Managed Environment" Error

If you see this error when trying to install packages:
```
error: externally-managed-environment
```

**Solution:** Use a virtual environment (see step 3 in Setup Instructions above).

This error occurs on newer Python installations (especially on macOS) that prevent installing packages globally. Virtual environments are the recommended way to manage Python dependencies.

### Port 5000 Already in Use

The app uses port 5001 by default. If you need to change it, edit `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=YOUR_PORT)
```

### API Key Errors

If you see "invalid x-api-key" errors:
1. Make sure your Anthropic API key is correct in the `.env` file
2. Ensure you have credits in your Anthropic account
3. Check that the key starts with `sk-ant-`

### Database Errors

If you encounter database errors, delete `nonprofit.db` and restart the app. It will create a fresh database.

## Contributing

Feel free to fork this project and submit pull requests!

## License

MIT License - Copyright (c) 2025 Vihaan Kava and Peiang

This project is open source and available for anyone to use and modify. See the [LICENSE](LICENSE) file for details.

## Support

For questions or issues, please open an issue on GitHub.

## Authors

- **Vihaan Kava** - [@vihaankava](https://github.com/vihaankava)
- **Peiang**

---

Built with ❤️ to help social entrepreneurs make a difference
