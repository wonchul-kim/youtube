import os
from dotenv import load_dotenv    
from youtube.utils.google_drive import get_folder_id, create_folder

load_dotenv('/HDD/github/youtube/.env')
YOUTUBE_SERVICE_ACCOUNT_FILE = os.getenv("YOUTUBE_SERVICE_ACCOUNT_FILE")

# goole_drive = GoogleDrive(YOUTUBE_SERVICE_ACCOUNT_FILE)

### 1 ===================================================================
folder_id = get_folder_id('매일경제tv', YOUTUBE_SERVICE_ACCOUNT_FILE)
print("📂 찾은 폴더 ID:", folder_id)


### 2 ===================================================================
folder_id = get_folder_id('Youtube', YOUTUBE_SERVICE_ACCOUNT_FILE)
create_folder('한경 글로벌마켓', YOUTUBE_SERVICE_ACCOUNT_FILE, folder_id)