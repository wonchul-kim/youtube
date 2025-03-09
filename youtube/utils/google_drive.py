import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload


def get_folder_id(folder_name, service_account_file, parent_folder_id=None, scopes=["https://www.googleapis.com/auth/drive.metadata.readonly",
                                                                                    "https://www.googleapis.com/auth/drive.file"]):
   
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    drive_service = build("drive", "v3", credentials=creds)
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"

    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]['id']  
    else:
        return None

def upload(filename, content, folder_name, service_account_file, scopes = ["https://www.googleapis.com/auth/drive.file"]):
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    drive_service = build("drive", "v3", credentials=creds)

    folder_id = get_folder_id(folder_name, service_account_file)
    assert folder_id is not None, RuntimeError(f"There is no such folder-id for '{folder_name}'")

    file_metadata = {
        "name": filename,
        "parents": [folder_id] 
    }
    
    if isinstance(content, str):
        file_stream = io.BytesIO(content.encode("utf-8"))
    elif isinstance(content, dict):
        import json
        file_stream = io.BytesIO(json.dumps(content, indent=4, ensure_ascii=False).encode("utf-8"))
        if 'json' not in filename:
            filename += '.json'
    else:
        raise NotImplementedError(f"NOT yet implement for {type(content)} type content")

    media = MediaIoBaseUpload(file_stream, mimetype="text/plain", resumable=True)

    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"✅ File({filename}) is SUCCESFULLY uploaded to Google Drive at {folder_name}")
    
    return True

def create_folder(folder_name, service_account_file, parent_folder_id=None, scopes = ["https://www.googleapis.com/auth/drive.file"]):
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    drive_service = build("drive", "v3", credentials=creds)
    
    folder_id = get_folder_id(folder_name, service_account_file)
    
    if folder_id:
        print(f"📂 폴더 '{folder_name}'가 이미 존재합니다. (ID: {folder_id})")
    else:
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parent_folder_id:
            file_metadata["parents"] = [parent_folder_id]

        folder = drive_service.files().create(body=file_metadata, fields="id").execute()
        folder_id = folder.get("id")
        print(f"✅ 폴더 '{folder_name}'를 생성했습니다. (ID: {folder_id})")

    return folder_id
