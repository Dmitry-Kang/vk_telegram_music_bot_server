# Bot for transfer vk music to telegram

This bot add ability to transfer music from vk to telegram
Supports download playlists(little buggy)
Do not requires vk boom subscription

## Project Setup

```sh
pip3 install -r requirements.txt
sudo apt install build-essential libssl-dev libffi-dev python-dev ffmpeg 
```
open database.db and insert your telegram id and vk id
open .env file and edit for your credits

### Run vk and tg bot(Both or only vk is required)

```sh
python3 vk.py
python3 tg.py
```
