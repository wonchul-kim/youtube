import os
from dotenv import load_dotenv    
from youtube.utils.google_drive import GoogleDrive

load_dotenv('/HDD/github/youtube/.env')
YOUTUBE_SERVICE_ACCOUNT_FILE = os.getenv("YOUTUBE_SERVICE_ACCOUNT_FILE")


google_drive = GoogleDrive(YOUTUBE_SERVICE_ACCOUNT_FILE)
### 1 ===================================================================
folder_id = google_drive.get_folder_id('매일경제TV')
print("📂 찾은 폴더 ID:", folder_id)


### 2 ===================================================================
folder_id = google_drive.get_folder_id('Youtube')
# google_drive.create_folder('한경 글로벌마켓', folder_id)
google_drive.create_folder('매일경제TV', folder_id)