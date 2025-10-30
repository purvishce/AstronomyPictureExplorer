import requests
import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
import asyncio
load_dotenv(override=True)

# Use DEMO_KEY if no key provided (rate limited)
nasa_api_key = os.getenv('NASA_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')


sytesmprompt = f"""You are an astrologer and have deep knowledge of the stars and the universe.Your explanation should be short — around 80-100 words — and sound like it could be told by a wise stargazer who sees both science and soul in the stars."""


openai = OpenAI()

def get_nasa_apod(date: str | None = None, hd: bool = False):
    """
    Fetch APOD and return (title, image_url, explanation).
    Handles errors and non-image media types gracefully.
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_api_key,
        "date": date,
        "hd": hd,
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        # If NASA returns 4xx/5xx, capture details from JSON if available
        if not response.ok:
            try:
                err = response.json()
                msg = err.get("error", {}).get("message") or str(err)
            except Exception:
                msg = response.text
            return ("Error fetching APOD", None, f"{response.status_code}: {msg}")

        data = response.json()
    except requests.exceptions.RequestException as e:
        return ("Network error", None, str(e))

    # Handle API-level errors returned in JSON
    if isinstance(data, dict) and "error" in data:
        msg = data.get("error", {}).get("message", "Unknown API error")
        return ("API error", None, msg)

    title = data.get("title", "Astronomy Picture of the Day")
    explanation = data.get("explanation", "")
    media_type = data.get("media_type", "image")

    if media_type == "image":
        image_url = data.get("hdurl") if hd and data.get("hdurl") else data.get("url")
        return (title, image_url, explanation)
    else:
        # For videos or other media types, no image to display
        media_url = data.get("url")
        note = f"This APOD is a {media_type}. Open in browser: {media_url}\n\n{explanation}"
        return (title, None, note)

def analyze_statement(title:str, image_url:str):
    prompt = f"""The following image is from NASA’s Astronomy Picture of the Day.
               Title: {title}               
                Create an explanation of the image in a way that is easy to understand and engaging.
              """
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": sytesmprompt}, {"role": "user", "content": prompt}])
    return response.choices[0].message.content


def app(date: str | None = None, hd: bool = False):
    """Gradio app wrapper for APOD."""
    title, image_url, explanation =  get_nasa_apod(date, hd)
    spacer = ""
    if image_url:
        analysis =  analyze_statement(title, image_url)
    else:
        analysis = explanation  # pass along note/explanation when not an image
    return title, image_url, analysis,spacer


#Define Interface
interface = gr.Interface(
    fn=app,
    inputs=[        
        gr.Textbox(label="Date (YYYY-MM-DD)", placeholder="Optional, leave blank for today"),
        gr.Checkbox(label="High Definition Image (HD)"),
    ],
    outputs=[
        gr.Markdown(label="Title"),
        gr.Image(label="NASA APOD Image"),
        gr.Textbox(label="Explanation from OpenAI-GPT-4o-mini", lines=5),
        
        
    ],
     title="🚀 NASA Astronomy Picture of the Day (APOD)",
    description="Enter optionally a date and check the HD checkbox to view the APOD in high definition and get the story from OpenAI-GPT-4o-mini."
)

if __name__ == "__main__":
   interface.launch()