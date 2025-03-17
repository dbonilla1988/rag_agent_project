import os
import requests
import openai
from dotenv import load_dotenv

# ---------- GOOGLE SEARCH ----------
def google_search(query):
    """Uses the Google Custom Search API to find info on a given query."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("GOOGLE_CSE_ID"),
        "q": query
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_google_response(json_data):
    """Extract title, snippet, and link from each search result item."""
    if "items" not in json_data:
        return []
    items = json_data["items"]
    parsed_results = []
    for item in items:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        parsed_results.append({
            "title": title,
            "snippet": snippet,
            "link": link
        })
    return parsed_results

# ---------- YOUTUBE SEARCH ----------
def youtube_search(query):
    """Uses the YouTube Data API to find trailer videos for a given query."""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": os.getenv("YOUTUBE_API_KEY"),
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 3
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_youtube_response(json_data):
    """Extract video title, channel, and URL from the YouTube search results."""
    items = json_data.get("items", [])
    videos = []
    for item in items:
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        videos.append({
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
    return videos

# ---------- (UPDATED) OPENAI SUMMARIZATION WITH ChatCompletion ----------
def summarize_results(google_res, youtube_res):
    """
    Sends a prompt to OpenAI ChatCompletion to summarize the combined Google + YouTube info.
    You need OPENAI_API_KEY in your .env for this to work.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Build a text block describing what we found
    google_text = "\n".join([f"- {g['title']}: {g['snippet']}" for g in google_res])
    youtube_text = "\n".join([f"- {y['title']} (Channel: {y['channel']})" for y in youtube_res])
    
    user_message = f"""
I searched for movie/series info and got the following Google results:
{google_text}

And these YouTube trailers:
{youtube_text}

Please provide a concise summary (3-5 sentences) of this movie/series based on this info.
    """.strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"Error calling OpenAI: {e}"

# ---------- MAIN FUNCTION ----------
def main():
    load_dotenv()  # Load .env variables

    # 1. Ask user for a movie/series name
    search_query = input("Enter a movie or series name: ")

    # 2. Google results (IMDB info, etc.)
    google_json = google_search(f"{search_query} imdb")
    google_results = parse_google_response(google_json)

    # 3. YouTube results (trailers)
    youtube_json = youtube_search(f"{search_query} official trailer")
    youtube_results = parse_youtube_response(youtube_json)

    # 4. Print results to console
    print("\n======== Google Info ========")
    if google_results:
        for i, g in enumerate(google_results, start=1):
            print(f"{i}. {g['title']}")
            print(f"   {g['snippet']}")
            print(f"   {g['link']}\n")
    else:
        print("No Google results found.")

    print("======== YouTube Trailers ========")
    if youtube_results:
        for i, vid in enumerate(youtube_results, start=1):
            print(f"{i}. {vid['title']}")
            print(f"   Channel: {vid['channel']}")
            print(f"   Link: {vid['url']}\n")
    else:
        print("No YouTube results found.")

    # 5. (Optional) Summarize with ChatGPT if you have a valid OPENAI_API_KEY
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and "sk-" in openai_key:
        print("======== OpenAI Summary ========")
        summary = summarize_results(google_results, youtube_results)
        print(summary)
    else:
        print("======== OpenAI Summary ========")
        print("No valid OPENAI_API_KEY found or it's not set up. Skipping summarization.")

if __name__ == "__main__":
    main()