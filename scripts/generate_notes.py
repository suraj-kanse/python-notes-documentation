#!/usr/bin/env python3
"""
Automated Daily Educational Notes Generator
Extracts transcripts from YouTube / local videos, breaks down content into distinct topics,
generates structured Markdown notes using Gemini, and updates the repository index.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = BASE_DIR / "notes"
QUEUE_FILE = BASE_DIR / "video_queue.txt"
README_FILE = BASE_DIR / "README.md"
MANIFEST_FILE = BASE_DIR / "generated_manifest.json"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def extract_youtube_video_id(url: str) -> str:
    """Extract YouTube Video ID from various URL formats."""
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [""])[0]
        if parsed.path.startswith(("/embed/", "/v/")):
            return parsed.path.split("/")[2]
    elif parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/").split("?")[0]
    return ""


def get_youtube_transcript(video_id: str) -> str:
    """Fetch transcript using youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Try fetching English, auto-generated, or Hindi transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except Exception:
            # Fallback to generated or any available language, or translated to en
            try:
                transcript = transcript_list.find_generated_transcript(['en', 'hi'])
                if transcript.language_code != 'en':
                    transcript = transcript.translate('en')
            except Exception:
                # Grab the first available transcript and translate if needed
                for t in transcript_list:
                    if t.is_translatable:
                        transcript = t.translate('en')
                        break
                    else:
                        transcript = t
                        break

        data = transcript.fetch()
        full_text = " ".join([entry.get('text', '') for entry in data])
        return full_text.strip()
    except Exception as e:
        print(f"[WARN] YouTube transcript API fetch failed: {e}")
        return ""


def download_audio_and_transcribe_gemini(video_url: str, api_key: str) -> str:
    """Download audio with yt-dlp and transcribe using Gemini File API."""
    import tempfile
    import yt_dlp
    
    print("[INFO] Attempting audio download & Gemini transcription...")
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tmpdir, 'audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        if not os.path.exists(audio_path):
            # Check for any generated audio file in tmpdir
            files = list(Path(tmpdir).glob("audio.*"))
            if files:
                audio_path = str(files[0])
            else:
                raise FileNotFoundError("Audio extraction failed with yt-dlp.")

        # Upload and transcribe via Gemini
        from google import genai
        client = genai.Client(api_key=api_key)
        uploaded_file = client.files.upload(file=audio_path)
        print(f"[INFO] Uploaded audio to Gemini File API (URI: {uploaded_file.uri})")
        
        prompt = "Transcribe the spoken audio in complete detail and return the raw transcribed text."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, prompt]
        )
        return response.text.strip() if response and response.text else ""


def generate_notes_with_gemini(transcript: str, video_title: str, video_url: str, api_key: str) -> list:
    """Call Gemini to break down the transcript into multiple topic markdown files."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are an expert technical educator and Python author specializing in creating high-quality, "
        "comprehensive, beginner-friendly yet technically deep educational notes for open-source repositories.\n"
        "Your task is to analyze the provided video transcript and break it down into distinct topics or sub-topics.\n"
        "For each topic/sub-topic, you must produce a separate structured markdown note.\n\n"
        "Each note MUST include:\n"
        "1. Conceptual Explanation with real-world analogies.\n"
        "2. Accurate, copy-pasteable Python code snippets explaining the concept.\n"
        "3. Common pitfalls / interview questions & edge cases.\n"
        "4. 'BTS / Under the Hood' memory and runtime explanation (reference counts, object mutability, etc. when applicable).\n"
        "5. Summary & Takeaways bullet list.\n\n"
        "Output MUST be valid JSON conforming strictly to the requested schema."
    )

    prompt = (
        f"Video Source: {video_url}\n"
        f"Video Context / Title: {video_title}\n\n"
        f"TRANSCRIPT CONTENT:\n{transcript[:40000]}\n\n"
        "Break this content down into 2 to 5 distinct topic files based on the natural segments of the video. "
        "Return a JSON array of objects with keys: 'topic_number' (integer starting from 1), "
        "'topic_title' (string), 'filename_slug' (kebab-case or snake_case string, e.g. '01_intro_to_oop'), "
        "'commit_message' (e.g. 'docs: add comprehensive notes on Object-Oriented Programming basics'), "
        "'summary' (1-2 sentence description), and 'markdown_content' (the complete markdown formatted note)."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.3
            )
        )
        text = response.text.strip()
        data = json.loads(text)
        if isinstance(data, dict) and "topics" in data:
            return data["topics"]
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"[ERROR] Failed to generate notes via Gemini: {e}")
        # Fallback to direct text parsing if JSON parse failed
        return []


def update_readme_index(created_files: list, video_url: str, date_str: str):
    """Update README.md with newly added notes."""
    if not README_FILE.exists():
        readme_content = "# Python Notes & Documentation\n\nAutomated daily notes generated from high-value tutorials and educational lectures.\n\n## 📚 Index of Topics\n\n| Date | Topic | Notes Link | Source |\n|---|---|---|---|\n"
    else:
        readme_content = README_FILE.read_text(encoding="utf-8")
        if "## 📚 Index of Topics" not in readme_content:
            readme_content += "\n\n## 📚 Index of Topics\n\n| Date | Topic | Notes Link | Source |\n|---|---|---|---|\n"

    new_rows = []
    for item in created_files:
        rel_path = os.path.relpath(item["file_path"], BASE_DIR).replace("\\", "/")
        title = item["title"]
        source_link = f"[Video]({video_url})" if video_url else "N/A"
        new_rows.append(f"| {date_str} | {title} | [{Path(rel_path).name}]({rel_path}) | {source_link} |")

    if new_rows:
        readme_content = readme_content.rstrip() + "\n" + "\n".join(new_rows) + "\n"
        README_FILE.write_text(readme_content, encoding="utf-8")
        print(f"[INFO] Updated README.md with {len(new_rows)} new topics.")


def process_video(video_url: str):
    """Main processing pipeline for a single video URL."""
    print(f"[INFO] Processing Video URL: {video_url}")
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = NOTES_DIR / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    video_id = extract_youtube_video_id(video_url)
    transcript = ""

    if video_id:
        print(f"[INFO] Extracted YouTube Video ID: {video_id}")
        transcript = get_youtube_transcript(video_id)

    if not transcript and GEMINI_API_KEY:
        print("[INFO] Subtitles not found via standard API, falling back to audio extraction...")
        try:
            transcript = download_audio_and_transcribe_gemini(video_url, GEMINI_API_KEY)
        except Exception as e:
            print(f"[WARN] Audio fallback failed: {e}")

    if not transcript:
        print("[ERROR] Could not extract transcript for this video. Exiting.")
        sys.exit(1)

    print(f"[INFO] Transcript obtained ({len(transcript)} characters). Generating notes...")
    
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Cannot run AI summarization.")
        sys.exit(1)

    topics = generate_notes_with_gemini(transcript, f"Video {video_id}", video_url, GEMINI_API_KEY)
    
    if not topics:
        print("[ERROR] No topics were generated by Gemini.")
        sys.exit(1)

    created_records = []
    for i, topic in enumerate(topics, 1):
        slug = topic.get("filename_slug", f"topic_{i}").replace(" ", "_").replace(":", "-")
        filename = f"{slug}.md" if not slug.endswith(".md") else slug
        target_path = output_dir / filename
        
        title = topic.get("topic_title", f"Topic {i}")
        commit_msg = topic.get("commit_message", f"docs: add notes on {title}")
        content = topic.get("markdown_content", "")

        # Write note file
        header = f"# {title}\n\n> **Source:** [{video_url}]({video_url})  \n> **Date:** {date_str}\n\n---\n\n"
        target_path.write_text(header + content, encoding="utf-8")
        print(f"[INFO] Generated note: {target_path}")

        created_records.append({
            "file_path": str(target_path),
            "title": title,
            "commit_message": commit_msg,
            "date": date_str
        })

    # Update README
    update_readme_index(created_records, video_url, date_str)

    # Save manifest for multi-commit automation
    MANIFEST_FILE.write_text(json.dumps({
        "video_url": video_url,
        "date": date_str,
        "created_files": created_records
    }, indent=2), encoding="utf-8")
    print(f"[INFO] Manifest saved to {MANIFEST_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Automated Educational Notes Generator")
    parser.add_argument("--url", type=str, help="Video URL to process")
    args = parser.parse_args()

    url = args.url
    if not url:
        # Check queue file
        if QUEUE_FILE.exists():
            lines = [l.strip() for l in QUEUE_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
            if lines:
                url = lines[0]
                # Update queue by removing the processed url
                remaining = "\n".join(lines[1:])
                QUEUE_FILE.write_text(remaining + ("\n" if remaining else ""), encoding="utf-8")
                print(f"[INFO] Popped URL from queue: {url}")

    if not url:
        print("[INFO] No URL provided and video_queue.txt is empty. Nothing to process.")
        sys.exit(0)

    process_video(url)


if __name__ == "__main__":
    main()
