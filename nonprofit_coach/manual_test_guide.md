# Manual Testing Guide for Tasks 1 & 2

This guide shows you how to manually test the nonprofit idea coach database layer using your Flask app.

## Step 1: Start the Flask Server

```bash
cd nonprofit_coach
python3 app.py
```

The server should start on `http://localhost:5000`

## Step 2: Test Creating an Idea

```bash
curl -X POST http://localhost:5000/api/test/ideas \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Community Food Bank",
    "description": "A food bank to serve low-income families",
    "importance": "Addresses food insecurity in our community",
    "beneficiaries": "Low-income families and seniors",
    "implementation": "Partner with local grocery stores for donations",
    "significance": "Will serve 500+ families monthly",
    "uniqueness": "Focus on fresh produce and nutrition education",
    "status": "draft"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "idea_id": 1,
  "idea": {
    "id": 1,
    "title": "Community Food Bank",
    "description": "A food bank to serve low-income families",
    ...
  }
}
```

## Step 3: Retrieve the Idea

```bash
curl http://localhost:5000/api/test/ideas/1
```

**Expected Response:**
```json
{
  "success": true,
  "idea": {
    "id": 1,
    "title": "Community Food Bank",
    ...
  }
}
```

## Step 4: Save Marketing Content

```bash
curl -X POST http://localhost:5000/api/test/ideas/1/content \
  -H "Content-Type: application/json" \
  -d '{
    "section": "marketing",
    "content_type": "email",
    "content": "Join us in fighting food insecurity! Our Community Food Bank is launching to serve 500+ families monthly with fresh produce and nutrition education."
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "content_id": 1
}
```

## Step 5: Save Team Content

```bash
curl -X POST http://localhost:5000/api/test/ideas/1/content \
  -H "Content-Type: application/json" \
  -d '{
    "section": "team",
    "content_type": "job_description",
    "content": "Volunteer Coordinator - Organize food distribution events and manage volunteer schedules. Must be passionate about community service."
  }'
```

## Step 6: Retrieve Marketing Content

```bash
curl http://localhost:5000/api/test/ideas/1/content/marketing
```

**Expected Response:**
```json
{
  "success": true,
  "content": [
    {
      "id": 1,
      "idea_id": 1,
      "section": "marketing",
      "content_type": "email",
      "content": "Join us in fighting food insecurity!...",
      "created_at": "2025-11-07 ..."
    }
  ]
}
```

## Step 7: Retrieve Team Content

```bash
curl http://localhost:5000/api/test/ideas/1/content/team
```

## Step 8: Add a Volunteer

```bash
curl -X POST http://localhost:5000/api/test/ideas/1/volunteers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "task": "Food sorting and distribution"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "volunteer_id": 1
}
```

## Step 9: Retrieve Volunteers

```bash
curl http://localhost:5000/api/test/ideas/1/volunteers
```

**Expected Response:**
```json
{
  "success": true,
  "volunteers": [
    {
      "id": 1,
      "idea_id": 1,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "555-1234",
      "address": "123 Main St",
      "task": "Food sorting and distribution",
      "created_at": "2025-11-07 ..."
    }
  ]
}
```

## Alternative: Use Postman or Browser

### Using Postman:
1. Import the requests above as a collection
2. Set the base URL to `http://localhost:5000`
3. Run each request in sequence

### Using Browser (for GET requests):
- Visit: `http://localhost:5000/api/test/ideas/1`
- Visit: `http://localhost:5000/api/test/ideas/1/content/marketing`
- Visit: `http://localhost:5000/api/test/ideas/1/volunteers`

## Test Routes Available

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/test/ideas` | Create a new idea |
| GET | `/api/test/ideas/<id>` | Get idea by ID |
| POST | `/api/test/ideas/<id>/content` | Save content for idea |
| GET | `/api/test/ideas/<id>/content/<section>` | Get content by section |
| POST | `/api/test/ideas/<id>/volunteers` | Add volunteer |
| GET | `/api/test/ideas/<id>/volunteers` | Get volunteers |

## Troubleshooting

**If you get "Module not found" errors:**
```bash
cd nonprofit_coach
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 app.py
```

**To check the database directly:**
```bash
sqlite3 nonprofit.db
.tables
SELECT * FROM ideas;
SELECT * FROM content;
SELECT * FROM volunteers;
.quit
```

**To reset the database:**
```bash
rm nonprofit.db
# Restart the Flask app - it will recreate the database
```
