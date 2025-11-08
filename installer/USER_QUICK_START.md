# Nonprofit Idea Coach - Quick Start Guide

## Installation

### Windows
1. Extract the ZIP file to any folder
2. Double-click **"start.bat"**
3. The app opens in your browser automatically

### Mac
1. Open the DMG file (or extract ZIP)
2. Double-click **"start.command"**
3. If you see a security warning:
   - Right-click on "start.command"
   - Select "Open"
   - Click "Open" again
4. The app opens in your browser automatically

## First Time Setup

1. **Enter Your API Key**
   - You'll be prompted for an Anthropic API key
   - Get one free at: https://console.anthropic.com
   - Choose whether to save it for future sessions

2. **Start Creating**
   - Click "Start New Idea"
   - Answer the guided questions
   - Let the AI help develop your nonprofit plan

## Using the Application

### Main Features

**1. Idea Development**
- Answer questions about your nonprofit idea
- Get AI-powered follow-up questions
- Build a comprehensive plan

**2. Section Tools**
After completing your idea, access four sections:
- **Research**: Find local organizations, resources, implementation steps
- **Team**: Create job descriptions, recruitment materials
- **Funding**: Generate grant proposals, budget plans
- **Marketing**: Create emails, flyers, social media posts

**3. AI Chat**
- Chat with AI in any section
- Get personalized advice
- Refine your content

### Tips for Best Results

✅ **Do:**
- Be specific in your answers
- Provide location information for local searches
- Save your work frequently (auto-saved)
- Use the chat feature to refine content

❌ **Avoid:**
- Vague or one-word answers
- Closing the browser while generating content
- Using multiple tabs for the same idea

## Configuration (Optional)

### Using the .env File

For advanced users who want to pre-configure settings:

1. Find the `.env.example` file in the installation folder
2. Copy it and rename to `.env`
3. Edit with any text editor
4. Add your API keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   BRAVE_API_KEY=your_brave_key_here  # Optional for web search
   ```
5. Restart the application

### Available Settings

```bash
# Required
ANTHROPIC_API_KEY=your_key_here

# Optional - Web Search (enhances research features)
SEARCH_PROVIDER=brave
SEARCH_ENABLED=true
BRAVE_API_KEY=your_brave_key_here

# Optional - Advanced
SECRET_KEY=your-secret-key
SEARCH_CACHE_TTL=86400
```

## Troubleshooting

### Application Won't Start

**Windows:**
- Make sure you extracted the ZIP file (don't run from inside ZIP)
- Check if port 5001 is available
- Try running as Administrator

**Mac:**
- Allow the app in Security & Privacy settings
- Make sure you have internet connection
- Check Console app for error messages

### Browser Doesn't Open

1. Manually open your browser
2. Go to: `http://localhost:5001`
3. Bookmark this address for easy access

### API Key Issues

**"API key not configured"**
- Enter your API key in the app
- Or add it to the `.env` file
- Restart the application

**"Invalid API key"**
- Verify your key at https://console.anthropic.com
- Make sure there are no extra spaces
- Check if your key has expired

### Content Generation Fails

**Check:**
- Internet connection is active
- API key is valid and has credits
- You're not hitting rate limits
- Try refreshing the page

### Search Features Not Working

- Search is optional and requires a Brave API key
- Get one at: https://brave.com/search/api/
- Add to `.env` file: `BRAVE_API_KEY=your_key`
- The app works fine without search (AI-only mode)

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh page
- **Ctrl/Cmd + W**: Close tab
- **Ctrl/Cmd + T**: New tab
- **Ctrl/Cmd + Click**: Open link in new tab

## Data Storage

### Where Your Data is Stored

- **Local Database**: `nonprofit.db` in the installation folder
- **Generated Sites**: `generated_sites/` folder
- **No Cloud Storage**: All data stays on your computer

### Backing Up Your Data

1. Close the application
2. Copy these files/folders:
   - `nonprofit.db`
   - `generated_sites/`
   - `.env` (if you created one)
3. Store in a safe location

### Restoring from Backup

1. Close the application
2. Replace the files with your backup copies
3. Restart the application

## Uninstalling

### Windows
1. Close the application
2. Delete the installation folder
3. Delete the desktop shortcut (if created)

### Mac
1. Close the application
2. Delete the installation folder
3. Remove from Applications folder (if linked)

## Getting Help

### Common Questions

**Q: Do I need to be online?**
A: Yes, the AI features require internet connection.

**Q: Is my data private?**
A: Yes, all data is stored locally. API calls go to Anthropic's servers per their privacy policy.

**Q: Can I use this offline?**
A: No, AI features require internet. You can view saved content offline.

**Q: How much does it cost?**
A: The app is free. You pay for Anthropic API usage (typically $0.25-$1.00 per session).

**Q: Can I export my content?**
A: Yes, copy from the browser or access files in `generated_sites/` folder.

**Q: Can multiple people use this?**
A: Yes, but one at a time. Each person can have their own installation.

### Support Resources

- **Documentation**: See README.md in installation folder
- **API Documentation**: https://docs.anthropic.com
- **Search API**: https://brave.com/search/api/docs

### Reporting Issues

If you encounter problems:

1. Check the troubleshooting section above
2. Note the error message (if any)
3. Check the console output for details
4. Contact support with:
   - Operating system and version
   - Error message
   - Steps to reproduce
   - Screenshots (if helpful)

## Tips for Success

### Writing Better Prompts

**Instead of:** "Help with marketing"
**Try:** "Create an email campaign for recruiting volunteers for a food bank in Seattle"

**Instead of:** "Need funding"
**Try:** "Generate a grant proposal for a youth mentorship program targeting at-risk teens, budget $50,000"

### Organizing Your Ideas

- Create separate ideas for different projects
- Use descriptive titles
- Complete all questionnaire fields
- Save important content externally

### Maximizing AI Quality

- Provide context in your questions
- Be specific about your needs
- Use the chat feature to iterate
- Review and edit AI-generated content

## Updates

### Checking for Updates

- Check the download page periodically
- Subscribe to update notifications (if available)

### Installing Updates

1. Download the new version
2. Close the old version
3. Backup your data (see above)
4. Install new version
5. Copy your `.env` file to new installation
6. Copy `nonprofit.db` to new installation

## Advanced Usage

### Running on a Different Port

Edit the startup script and change `5001` to your preferred port.

### Using with Multiple Browsers

The app works with any modern browser:
- Chrome
- Firefox
- Safari
- Edge

### Accessing from Other Devices

By default, the app only runs locally. To access from other devices on your network:
1. This requires code changes (not recommended for beginners)
2. Consider security implications
3. Consult technical documentation

---

**Version**: 1.0.0  
**Last Updated**: 2024

**Enjoy building your nonprofit idea! 🚀**
