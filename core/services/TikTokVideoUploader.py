from core.interfaces.IVideoUploader import IVideoUploader
import os
import requests
from config import VIDEO_PATH

class TikTokVideoUploader(IVideoUploader):
    def __init__(self):
        self.API_BASE = "https://open.tiktokapis.com/v2/"


    def publish(self, token: str, publish_id: str, title: str = "Meu Vídeo") -> str:
        url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/complete/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "publish_id": publish_id,
            "post_info": {
                "title": title,
                "privacy_level": "PUBLIC",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return f"https://www.tiktok.com/@me/video/{publish_id}"


    def upload(self, access_token: str) -> str:
        video_size = os.path.getsize(VIDEO_PATH)

        init_payload = {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1
            }
        }

        init_res = requests.post("https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
                                 headers={
                                     "Authorization": f"Bearer {access_token}",
                                     "Content-Type": "application/json"
                                 },
                                 json=init_payload)

        init_data = init_res.json()
        if init_data.get("error", {}).get("code") != "ok":
            raise Exception(f"Erro ao iniciar upload: {init_data}")

        upload_url = init_data["data"]["upload_url"]
        publish_id = init_data["data"]["publish_id"]

        with open(VIDEO_PATH, "rb") as f:
            video_data = f.read()
        content_range = f"bytes 0-{video_size - 1}/{video_size}"
        upload_res = requests.put(upload_url,
                                  headers={"Content-Type": "txt",
                                           "Content-Range": content_range},
                                  data=video_data)

        if upload_res.status_code != 200:
            raise Exception(f"Erro ao enviar vídeo: {upload_res}")

        return publish_id
