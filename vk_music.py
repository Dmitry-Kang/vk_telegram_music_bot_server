from vk_api import audio
import vk_api

class VKmusic:
    def __init__(self, login, password, token):
        self.session = vk_api.VkApi(login=login , password=password , token=token)
        self.session.auth()
        self.vk_music = audio.VkAudio(self.session)

