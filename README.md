# Nonprofit Idea Coach

An AI-powered tool that helps you develop nonprofit ideas into actionable startup plans with personalized websites.

## Features

- 🤖 AI-guided questionnaire to develop your nonprofit idea
- 🎨 Automatically generated personalized website for each nonprofit
- 📚 Research & Planning tools (implementation steps, local orgs, resources)
- 👥 Team Building tools (recruiting pitch, job descriptions, volunteer forms)
- 💰 Funding Strategy tools (grant proposals, donor letters, budget plans)
- 📢 Marketing Materials (emails, flyers, social media posts)
- 💬 AI chat assistant for each section
- 🗑️ Easy idea management with delete functionality

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

2. **Install Python dependencies:**
   ```bash
   cd nonprofit_coach
   pip3 install flask anthropic python-dotenv
   ```

3. **Set up your API key:**
   
   Open the `.env` file and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   SECRET_KEY=your-secret-key-change-in-production
   ```

4. **Run the application:**
   ```bash
   python3 app.py
   ```

5. **Open your browser:**
   
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
- **Frontend**: HTML, CSS, JavaScript (vanilla)

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

## Troubleshooting

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

This project is open source and available for anyone to use and modify.

## Support

For questions or issues, please open an issue on GitHub.

---

Built with ❤️ to help social entrepreneurs make a difference
