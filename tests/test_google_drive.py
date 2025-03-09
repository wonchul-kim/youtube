import os
from dotenv import load_dotenv    
from youtube.utils.google_drive import get_folder_id

load_dotenv('/HDD/github/youtube/.env')
YOUTUBE_SERVICE_ACCOUNT_FILE = os.getenv("YOUTUBE_SERVICE_ACCOUNT_FILE")

folder_name = '매일경제tv'
folder_id = get_folder_id(folder_name, YOUTUBE_SERVICE_ACCOUNT_FILE)
print("📂 찾은 폴더 ID:", folder_id)


