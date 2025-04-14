from adapters import flask_web_server
from utils.browser_utils import open_browser
from core.services.TikTokAuthorizationService import TikTokAuthorizationService
from core.services.TikTokVideoUploader import TikTokVideoUploader

def main():
    flask_web_server.start_flask()

    auth_service = TikTokAuthorizationService()
    uploader = TikTokVideoUploader()

    auth_url = auth_service.generate_auth_url()
    open_browser(auth_url)

    code = flask_web_server.wait_for_code()
    token = auth_service.get_access_token(code)

    if token:
        publish_id = uploader.upload(token) # Faz o upload do vídeo
        video_url = uploader.public(token, publish_id) # Publica o vídeo
        print(f">> Vídeo enviado com sucesso!\n>> Publish ID: {publish_id} || >> URL: {video_url}")

if __name__ == "__main__":
    main()
