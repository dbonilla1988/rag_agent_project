import os
import tkinter as tk
from tkinter import scrolledtext

# Import your RAG logic (google_search, youtube_search, parse, etc.)
import requests
import openai
from dotenv import load_dotenv

###############################
# Example RAG Logic Functions #
###############################

def google_search(query):
    # Example only; adapt to your actual code
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("GOOGLE_CSE_ID"),
        "q": query
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_google_response(json_data):
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

def youtube_search(query):
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

def summarize_results(google_res, youtube_res):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    google_text = "\n".join([f"- {g['title']}: {g['snippet']}" for g in google_res])
    youtube_text = "\n".join([f"- {y['title']} (Channel: {y['channel']})" for y in youtube_res])
    
    prompt = f"""
    I searched for movie/series info and got the following Google results:
    {google_text}

    And these YouTube trailers:
    {youtube_text}

    Please provide a concise summary (3-5 sentences) based on this info.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=150,
            temperature=0.7
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"Error calling OpenAI: {e}"


######################
# Tkinter GUI Section #
######################

def run_query():
    """Triggered by the 'Search' button. Fetch Google & YouTube, display results, optionally summarize."""
    query = query_entry.get().strip()
    if not query:
        return

    # Clear previous output
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)

    # Perform Google Search
    google_data = google_search(query + " imdb")  # e.g., "Inception imdb"
    google_results = parse_google_response(google_data)

    # Perform YouTube Search
    youtube_data = youtube_search(query + " official trailer")
    youtube_results = parse_youtube_response(youtube_data)

    # Display Google Results
    output_area.insert(tk.END, "======== Google Info ========\n")
    if google_results:
        for i, g in enumerate(google_results, start=1):
            output_area.insert(tk.END, f"{i}. {g['title']}\n   {g['snippet']}\n   {g['link']}\n\n")
    else:
        output_area.insert(tk.END, "No results found.\n\n")

    # Display YouTube Results
    output_area.insert(tk.END, "======== YouTube Trailers ========\n")
    if youtube_results:
        for i, vid in enumerate(youtube_results, start=1):
            output_area.insert(tk.END, f"{i}. {vid['title']}\n   Channel: {vid['channel']}\n   Link: {vid['url']}\n\n")
    else:
        output_area.insert(tk.END, "No trailers found.\n\n")

    # If OpenAI key is present, do a summary
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key.startswith("sk-"):
        summary = summarize_results(google_results, youtube_results)
        output_area.insert(tk.END, "======== OpenAI Summary ========\n")
        output_area.insert(tk.END, f"{summary}\n\n")
    else:
        output_area.insert(tk.END, "======== OpenAI Summary ========\n")
        output_area.insert(tk.END, "No valid OPENAI_API_KEY, skipping summary.\n\n")

    output_area.config(state=tk.DISABLED)

def main():
    load_dotenv()

    # Initialize the tkinter window
    root = tk.Tk()
    root.title("RAG Agent")

    # Label + text entry for user queries
    tk.Label(root, text="Enter movie/series:").pack()
    global query_entry
    query_entry = tk.Entry(root, width=50)
    query_entry.pack()

    # Search button
    tk.Button(root, text="Search", command=run_query).pack()

    # Scrolled text area for displaying results
    global output_area
    output_area = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.NORMAL)
    output_area.pack()

    # Main event loop
    root.mainloop()

if __name__ == "__main__":
    main()