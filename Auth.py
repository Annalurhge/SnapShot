from firebase_admin import storage, firestore, credentials, auth, initialize_app
import os
from icecream import ic
import datetime
import hashlib

class FirebaseAuthentication:
    def __init__(self):
        self.album_id = "89127391823"
        
        firebase_credentials_json = {
        }
        self.cred = credentials.Certificate(firebase_credentials_json)
        initialize_app(self.cred)
        self.db = firestore.client()
    
    def create_new_album(self, user, folder):
        album_data = {
            "created_at"    : f"{datetime.datetime.now()}",
            "title"         : f"{folder}",
            "user_id"       : f"{user}"
        }
        
        doc_ref = self.db.collection("albums").document()
        self.album_id = doc_ref.id
        
        doc_ref.set(album_data)
    
    def create_new_screenshot(self, cloud_url):
        screnshot_data = {
            "album_id"          : f"{self.album_id}",
            "created_at"        : f"{datetime.datetime.now()}",
            "screenshot_url"    : f"{cloud_url}",
        }
        
        doc_ref = self.db.collection("screenshots").document()
        
        doc_ref.set(screnshot_data)
    def sign_in_with_email(self, email, password):
        try:
            users_ref = self.db.collection("users")
            docs = users_ref.stream()
            
            # Sign in with email and password 
            user = auth.get_user_by_email(email)
            pull_password = [doc.to_dict() for doc in docs if doc.id == user.uid][0]["password"]
            if password == pull_password:
                return user.uid, user.email
            return None, None
        except Exception as e:
            # print("Error signing in with email:", e)
            return None, None
    
    def upload_folder_to_storage(self, folder_path, user_id):
        bucket_name = "snapshot-12194.appspot.com"
        bucket = storage.bucket(bucket_name)
        
        # blob.upload_from_string("", content_type='text/plain')
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.relpath(local_file_path, folder_path)
                blob = bucket.blob(f"{user_id}/{self.album_id}/{remote_file_path}")
                blob.upload_from_filename(local_file_path)
                print(f"Uploaded {local_file_path} to {blob.public_url}")
        
        blob = bucket.blob(f"{user_id}/{root}/")
        self.create_new_screenshot(blob.path)
    