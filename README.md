# RAG Agent Project

A simple Retrieval-Augmented Generation (RAG) agent that fetches movie or series information from Google (using the Custom Search API) and YouTube (using the YouTube Data API), then summarizes the results with OpenAI.

## Features
- **Google Search Integration:** Retrieves IMDB-like info about movies/series.
- **YouTube Search Integration:** Fetches trailers from YouTube.
- **OpenAI Summarization:** Uses ChatGPT to summarize the found information.
- **Command-Line Interface:** Prompts for a movie/series title and displays results in the terminal.

## Requirements and Installation

1. **Python 3.7+** (recommended)
2. **Virtual Environment** (optional but recommended)

**Steps to install:**

```bash
# 1. Clone this repository
git clone https://github.com/YourUsername/rag_agent_project.git
cd rag_agent_project

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

Configuration (.env File)

Create a file named .env in the project’s root directory with the following variables:

GOOGLE_API_KEY=YourGoogleApiKey
GOOGLE_CSE_ID=YourGoogleCseId
YOUTUBE_API_KEY=YourYouTubeApiKey
OPENAI_API_KEY=sk-YourOpenAiKey



GOOGLE_API_KEY: Created in Google Cloud Console after enabling the Custom Search API
	•	GOOGLE_CSE_ID: From your Programmable Search Engine dashboard
	•	YOUTUBE_API_KEY: Generated in the Google Cloud Console by enabling the YouTube Data API v3

	Usage
	1.	Activate your virtual environment (if created).
	2.	Run the script:

	python main.py

	3.	Enter a movie or series name when prompted (e.g., “Inception”).

Example Output


Enter a movie or series name: Inception

======== Google Info ========
1. Inception (2010) - IMDb
   A thief who steals corporate secrets...
   https://www.imdb.com/title/tt1375666/

======== YouTube Trailers ========
1. Inception - Official Trailer [HD]
   Channel: Warner Bros. Pictures
   Link: https://www.youtube.com/watch?v=8hP9D6kZseM

======== OpenAI Summary ========
"Inception" is a sci-fi thriller directed by Christopher Nolan...



rag_agent_project/
  ├─ venv/              # (virtual environment, optional)
  ├─ .env               # API keys (excluded from Git)
  ├─ requirements.txt   # dependencies
  ├─ main.py            # main script
  └─ README.md          # this documentation