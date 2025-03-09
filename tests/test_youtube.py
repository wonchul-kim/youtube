import os
from dotenv import load_dotenv    
from youtube.utils.google_drive import upload
from youtube.utils.youtube import get_youtube_video_data

load_dotenv('/HDD/github/youtube/.env')
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SERVICE_ACCOUNT_FILE = os.getenv("YOUTUBE_SERVICE_ACCOUNT_FILE")
youtube_channel_name = '매일경제tv'
url = "https://www.youtube.com/watch?v=GSqGXQP52GE"

save_dir = '/HDD/etc'
data = get_youtube_video_data(url, YOUTUBE_API_KEY, save_dir)
print(data)

upload('abcd', data, youtube_channel_name, YOUTUBE_SERVICE_ACCOUNT_FILE)
