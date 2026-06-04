from urllib.parse import urlparse, parse_qs
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=st.secrets["WEBSHARE_USERNAME"],
        proxy_password=st.secrets["WEBSHARE_PASSWORD"],
    )
)

def extract_video_id(url):
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]

    if "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    return None

def get_transcript(url):
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript = ytt_api.fetch(video_id)

    return " ".join([entry.text for entry in transcript])