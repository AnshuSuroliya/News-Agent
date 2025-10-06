# News Aggregator ADK

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd news-aggregator-adk/news_aggregator_adk
```

### 2. Install Python Dependencies
```
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file in the project root (same directory as `main.py`) with the following content:
```
NEWSAPI_KEY=your_newsapi_key_here
GOOGLE_API_KEY=your_google_api_key_here
GNEWS_API_KEY=your_gnews_api_key_here
```
Replace the values with your actual API keys.

### 4. Run the Backend (CLI)
```
python main.py
```
You will be prompted to enter your news query in the terminal.

---

## Project Structure
- `main.py` — Main entry point for CLI usage
- `fastapi_app.py` — FastAPI backend for API usage
- `agents/` — All agent definitions (router, specialized, report writer, audit)
- `tools/` — News fetching tools (NewsAPI, GNews, Google News RSS)
- `frontend/` — React UI (optional)
- `.env` — API keys (not committed to version control)

---

## Requirements
- Python 3.12+
- Node.js & npm (for frontend)
- API keys for NewsAPI, GNews, and Google Gemini

---

## Notes
- All news and audit reports are saved to `news_report.txt` and `audit_report.txt` after each run.
- The system is robust and will always provide some news, even if one or more APIs are down.

---

For more details, see the in-depth documentation in the codebase or contact the maintainer. 