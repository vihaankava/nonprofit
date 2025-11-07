# Version History

## v1.0-working (Current)

**Date:** November 7, 2025

**Status:** ✅ Fully Working

### Features
- AI-powered questionnaire with follow-up questions
- Dynamic website generation for each nonprofit idea
- Four sections: Research, Team, Funding, Marketing
- Content generation buttons for each section type
- AI chat assistant for iterative refinement
- Delete functionality for ideas and generated sites
- API key management (session + environment variable)
- Database integration with SQLite

### How to Restore This Version

If you need to go back to this working version:

```bash
# View all tags
git tag

# Restore to this version
git checkout v1.0-working

# Or create a new branch from this version
git checkout -b restore-v1.0 v1.0-working
```

### Running the Application

1. Navigate to the nonprofit_coach directory:
   ```bash
   cd nonprofit_coach
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key in `.env`:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

4. Run the application:
   ```bash
   python3 app.py
   ```

5. Open your browser to: http://127.0.0.1:5001

### Testing

- All features have been manually tested and verified working
- Content generation works with Claude API
- Delete functionality removes ideas and generated sites
- Chat assistant provides contextual help

---

## Future Versions

Document new versions below as you make changes.
