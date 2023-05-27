import requests, os
import vka.vk_commands as vk_commands
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from dotenv import load_dotenv
import vk_music
import vka.vk_utils as vk_utils
import tg
import traceback
import db
import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()

load_dotenv()

vk_session = vk_api.VkApi(login=os.getenv('VK_LOGIN') , password=os.getenv('VK_PASSWORD') , token=os.getenv('VK_TOKEN'))

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
vk_audio = vk_music.VKmusic(os.getenv('VK_LOGIN'), os.getenv('VK_PASSWORD'), os.getenv('VK_TOKEN')).vk_music

vk_utils.send_message_peer(vk, peer_id = os.getenv('VK_ADMIN_ID'), message = "LongPoll запущен")
def start1():
  indx = 0
  for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user and event.attachments and event.peer_id:
          user_db = db.getUser(event.peer_id)
          if not user_db:
              vk_utils.send_message_user(vk, user_id=event.user_id, message='Вы не авторизованы')
              return
          cnt_attachments = int(len(event.attachments) / 2) + 1
          
          attach_index = 1
          for attach_index in range(1, cnt_attachments):
              if (event.attachments.get(f"attach{attach_index}_type") and event.attachments.get(f"attach{attach_index}")):
                  # audio
                  if (event.attachments.get(f"attach{attach_index}_type") == 'audio'):
                      vk_utils.send_message_user(vk, user_id=event.user_id, message=event.attachments.get(f"attach{attach_index}"))
                      vk.messages.setActivity(type='typing', peer_id=event.peer_id)
                      name_audio, path_audio = vk_commands.download_track(vk_audio, event.attachments.get(f"attach{attach_index}"),indx)
                      indx += 1
                    #   print(name_audio, path_audio)
                    #   path = f"{os.getenv('AUDIO_DIRECTORY')}{name_audio}.mp3"
                      tg.send_audio_sync(user_db['tg_id'], path_audio)
                      vk_utils.send_message_user(vk, user_id=event.user_id, message='Готово')

                  # playlist '427589676_11'
                  if (event.attachments.get(f"attach{attach_index}_type") == 'audio_playlist'):
                      args_raw = event.attachments.get(f"attach{attach_index}")
                      args = args_raw.split("_")
                      # albums = vk_audio.get_albums(args[0]) # это нетрогаю т.к. нашел аналог для поиска album_title
                      # album_title = None
                      # for album in albums:
                      #     if album['id'] == args[1]:
                      #         album_title = album

                      try:
                          audios = vk_audio.get(owner_id=args[0], album_id=args[1])
                      except requests.exceptions.JSONDecodeError:
                          vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Произошла ошибка при получении списка треков из альбома {args_raw}.')
                          return
                      except vk_api.exceptions.AccessDenied:
                          vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Автор ограничил доступ к плейлисту {args_raw}.')
                          return

                      page = http.request('GET', f"https://m.vk.com/audio?act=audio_playlist{args_raw}")
                      soup = BeautifulSoup(page.data, 'html.parser')
                      total_sum_tracks_with_broken = soup.find('div', {'class': 'audioPlaylist__footer'}).text.split(" ")[0]
                      album_title = soup.find('div', {'class': 'audioPlaylist__title'}).text.strip()
                      print(str(album_title))

                      for audio in audios:
                          name_audio = vk_commands.download_track(vk_audio, f"{audio['owner_id']}_{audio['id']}", indx)
                          indx += 1
                      vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Готово {indx} из {total_sum_tracks_with_broken}')
                      return
                  
                  # video '228620070_456245187'
                  # if (event.attachments.get(f"attach{attach_index}_type") == 'audio'):
                  #     pass
          
      if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
          if event.from_user: #Если написали в ЛС 
              args_raw = event.message
              args = args_raw.split(" ")
              if not args[0].startswith("/"): # просто текст(возвращает айдишник)
                  vk.messages.send(
                          user_id=event.user_id,
                          random_id=0,
                          message=event.peer_id,
                          reply_to=event.message_id,
                      )
              else:                              # команда
                  args[0] = args[0].replace("/", "")
                  vk_utils.send_message_user(vk, user_id=event.user_id, message=f'1, {str(args)}')
                  if args[0] == "album": # загрузка альбома
                      if len(args) != 3:
                          vk_utils.send_message_user(vk, user_id=event.user_id, message='Нужны 2 аргумента + комманда. Пример: /album 427589676_11 SOMEHASH')
                          return
                      args2_raw = args[1]
                      args2 = args2_raw.split("_")
                      try:
                          audios = vk_audio.get(owner_id=args2[0], album_id=args2[1], access_hash=args[2])
                      except requests.exceptions.JSONDecodeError:
                          vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Произошла ошибка при получении списка треков из альбома {args2_raw}.')
                          return
                      except vk_api.exceptions.AccessDenied:
                          vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Автор ограничил доступ к плейлисту {args2_raw}.')
                          return

                      # page = http.request('GET', f"https://m.vk.com/audio?act=audio_playlist{args2_raw}")
                      # soup = BeautifulSoup(page.data, 'html.parser')
                      # total_sum_tracks_with_broken = soup.find('div', {'class': 'audioPlaylist__footer'}).text.split(" ")[0]
                      # album_title = soup.find('div', {'class': 'audioPlaylist__title'}).text.strip()
                      # print(str(album_title))

                      for audio in audios:
                          name_audio = vk_commands.download_track(vk_audio, f"{audio['owner_id']}_{audio['id']}", indx)
                          indx += 1
                      vk_utils.send_message_user(vk, user_id=event.user_id, message=f'Готово {indx} из {123}')
                      return

def start():
  while True:
    try:
      start1()
    except Exception as e:
      tg.send_message_sync(os.getenv('TG_ADMIN_ID'), f"vk: \n{traceback.format_exc()}")
start()
