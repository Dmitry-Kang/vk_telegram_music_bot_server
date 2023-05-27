#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Скрипт выводит в консоль содержимое файла в двоичном виде
# Можно использовать перенаправление вывода для сохранения файла
# Использование vkontakte_m3u8_downloader.py ссылка на аудиозапись > имя файла
# Для работы скрипта нужен ffmpeg
import re
import os.path
import sys
import tempfile
import subprocess
import requests

regex = "https.*key.pub"
regex_2 = '"https.*pub?.*"'
regex_3 = 'ts?.*'


def parse_m3u8(url):
    urldir = os.path.dirname(url)
    playlist = requests.get(url).text
    keyurl = re.findall(regex, playlist)[0]
    key = requests.get(keyurl).text

    for match in re.finditer(regex_2, playlist, re.MULTILINE):
        playlist = playlist.replace(match.group(), 'key.pub')

    for match in re.finditer(regex_3, playlist):
        playlist = playlist.replace(match.group(), 'ts')

    return playlist, key, urldir


def download_m3u8(playlist, key, urldir, output='out.ts'):
    ts_list = [x for x in playlist.split('\n') if not x.startswith('#')]

    with tempfile.TemporaryDirectory(output) as dir_:
        os.chdir(dir_)
        for file in ts_list[:-1]:
            with open(file, 'wb') as audio:
                audio.write(requests.get(os.path.join(urldir, file)).content)
        with open('key.pub', 'w') as keyfile:
            keyfile.write(key)
        with open('index.m3u8', 'w') as playlist_file:
            playlist_file.write(playlist)

        subprocess.call(['ffmpeg', '-allowed_extensions', "ALL", '-protocol_whitelist',
                         "crypto,file", '-i', 'index.m3u8', '-c', 'copy', f'{output}'])

        return open(output, 'rb').read()


if __name__ == '__main__':
    url = sys.argv[1]
    result = parse_m3u8(url)
    sys.stdout.buffer.write(download_m3u8(*result))
