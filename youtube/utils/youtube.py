import os.path as osp
import os
import re
import requests
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_youtube_metadata(video_id, API_KEY):
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=snippet"
    response = requests.get(url)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        snippet = data["items"][0]["snippet"]
        return snippet
    else:
        return None

def get_youtube_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        print("❌ 유효한 유튜브 URL이 아닙니다.")
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        formatter = TextFormatter()
        script_text = formatter.format_transcript(transcript)
        return script_text
    except Exception as e:
        print(f"❌ 자막을 가져오는 데 실패했습니다: {e}")
        return None
    
def get_youtube_video_data(url, api_key, save_dir=None):
    video_id = extract_video_id(url)
    
    data = get_youtube_metadata(video_id, api_key)
    data.update({"transcript": get_youtube_transcript(url)})

    if save_dir and osp.exists(save_dir):
        import json 
        with open(osp.join(save_dir, 'a.json'), "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return data


