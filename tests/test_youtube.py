import os
from dotenv import load_dotenv    
from youtube.utils.google_drive import upload
from youtube.utils.youtube import get_youtube_video_data, extract_channel_id, get_videos_from_channel

load_dotenv('/HDD/github/youtube/.env')
GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
YOUTUBE_SERVICE_ACCOUNT_FILE = os.getenv("YOUTUBE_SERVICE_ACCOUNT_FILE")

### 1 ==================================================================
# youtube_channel_name = '매일경제tv'
# url = "https://www.youtube.com/watch?v=GSqGXQP52GE"

# save_dir = '/HDD/etc'
# data = get_youtube_video_data(url, GOOGLE_CLOUD_API_KEY, save_dir)
# print(data)

# upload('abcd', data, youtube_channel_name, YOUTUBE_SERVICE_ACCOUNT_FILE)


### 2 ==================================================================
url = "https://www.youtube.com/@hkglobalmarket"
channe_id = extract_channel_id(url, GOOGLE_CLOUD_API_KEY)
print(channe_id)

from datetime import datetime 
published_after = datetime(2024, 3, 5, 15, 30).isoformat("T") + "Z"

videos = get_videos_from_channel(url, GOOGLE_CLOUD_API_KEY)#, published_after)

for video in videos:
    data = get_youtube_video_data(video['url'], GOOGLE_CLOUD_API_KEY)
    print(data)
