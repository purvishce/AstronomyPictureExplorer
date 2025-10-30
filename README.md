### Project: NASA Astronomy Picture Explorer + AI Narrator

A lightweight Gradio app that fetches NASA’s Astronomy Picture of the Day (APOD) and generates a concise, human-friendly narration using OpenAI. Supports HD images, date selection, graceful handling of videos, and clear error messages.

<img width="2048" height="1110" alt="image" src="https://github.com/user-attachments/assets/7543bb68-f13e-42f3-91e5-d65b51d47277" />


## Features
- Fetch APOD by date with optional HD image
- AI-generated 80–100 word explanation in a stargazer’s voice
- Handles non-image media with a link and note
- Clean Gradio UI with title, image, and AI narration
- Robust error messages for API/network issues

## Tech Stack
- Python, Gradio, Requests
- OpenAI API
- NASA APOD API

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set environment variables (use a `.env` file or your shell):
```bash
NASA_API_KEY=your_nasa_key   # falls back to DEMO_KEY if not set
OPENAI_API_KEY=your_openai_key
```

## Run
```bash
python week2/MyProjects/AstronomyPictureExplorer.py
```

## Usage
- Enter a date as YYYY-MM-DD (or leave blank for today)
- Toggle HD for higher-resolution images (when available)
- Read the AI narration below the image

## Notes
- If APOD is a video, the image is omitted and a link is provided.
- Using `DEMO_KEY` for NASA is rate-limited; get a free key from `https://api.nasa.gov`.

## Acknowledgements
- NASA APOD API
- OpenAI
- Gradio
