# RAG Agent Project

A simple **Retrieval-Augmented Generation (RAG)** agent that fetches movie or series information from **Google** (using the Custom Search API) and **YouTube** (using the YouTube Data API), then summarizes the results with **OpenAI** (ChatGPT). The project features both a command-line interface and a simple GUI built with Tkinter.

---

## Features

- **Google Search Integration:** Retrieves IMDB-like info for movies/series.
- **YouTube Search Integration:** Fetches trailer links from YouTube.
- **OpenAI Summarization:** Uses GPT-based models (ChatGPT) to generate a concise summary.
- **Graphical User Interface (GUI):** A simple Tkinter GUI that allows users to:
  - Enter a movie/series name.
  - Click a "Search" button to trigger the RAG process.
  - View results in a scrolling text area that displays:
    - The query (human input).
    - Google search results (titles, snippets, and links).
    - YouTube trailer links (video title, channel, and URL).
    - An optional OpenAI summary of the results.

---

## Requirements and Installation

1. **Python 3.7+** (recommended)  
2. **Virtual Environment** (optional but recommended)

### Steps to Install:

```bash
# 1. Clone this repository
git clone https://github.com/dbonilla1988/rag_agent_project.git
cd rag_agent_project

# 2. Create and activate a virtual environment using the official Python (recommended)
python3 -m venv newvenv
source newvenv/bin/activate  # macOS/Linux
# or on Windows:
newvenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt