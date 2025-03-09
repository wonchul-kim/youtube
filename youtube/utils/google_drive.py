import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload


class GoogleDrive:
    def __init__(self, service_account_file, 
                 scopes=["https://www.googleapis.com/auth/drive.metadata.readonly",
                         "https://www.googleapis.com/auth/drive.file"]):
        
        creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
        self.drive_service = build("drive", "v3", credentials=creds)
            
    def get_folder_id(self, folder_name, parent_folder_id=None):
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        # print(f"📌 Query: {query}")  # 쿼리 출력해서 확인!

        results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get("files", [])

        if folders:
            print(f"✅ 폴더 찾음: {folders[0]}")
            return folders[0]['id']
        else:
            print(f"❌ 폴더 '{folder_name}'를 찾을 수 없음")
            return None

    def delete_file_id(self, file_id):
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
            print(f"File {file_id} has been deleted.")
        except Exception as error:
            print(f"An error occurred: {error}")
            
    def delete_file(self, name):
        try:
            while True:
                id = self.get_folder_id(name)
                if id is None:
                    break
                self.drive_service.files().delete(fileId=id).execute()
                print(f"File {name} has been deleted.")
        except Exception as error:
            raise RuntimeError(f"An error occurred: {error}")

        
    def create_folder(self, folder_name, parent_folder_id=None):
        
        if len(folder_name.split("/")) > 1:
            self.get_or_create_folder_by_path(folder_name, parent_folder_id)
 
        folder_id = self.get_folder_id(folder_name, parent_folder_id=parent_folder_id)
        
        if folder_id:
            print(f"📂 폴더 '{folder_name}'가 이미 존재합니다. (ID: {folder_id})")
        else:
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder"
            }
            if parent_folder_id:
                file_metadata["parents"] = [parent_folder_id]

            folder = self.drive_service.files().create(body=file_metadata, fields="id").execute()
            folder_id = folder.get("id")
            print(f"✅ 폴더 '{folder_name}'를 생성했습니다. (ID: {folder_id})")

        return folder_id

    def get_or_create_folder_by_path(self, folder_path, parent_folder_id=None):
        folders = folder_path.split("/")

        for folder in folders:
            parent_folder_id = self.create_folder(folder, parent_folder_id) 

        return parent_folder_id
    
    def upload(self, filename, content, folder_name):
        folder_id = self.get_folder_id(folder_name)
        
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

        uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"✅ File({filename}) is SUCCESFULLY uploaded to Google Drive at {folder_name}")
        
        return True
