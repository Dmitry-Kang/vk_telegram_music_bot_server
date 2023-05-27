
import os
import vka.vkontakte_m3u8_downloader as vkontakte_m3u8_downloader
import vka.m3u82mp3 as m3u82mp3
import urllib.request

def download_track(vk_audio, text, index):
    # get audio info and m3u8
    args = text.split('_')
    res = vk_audio.get_audio_by_id(args[0], args[1])
    res = {'url': res.get('url'), 'artist': res.get('artist'), 'title': res.get('title')}
    if "?" in res['url']:
        res['url'] = res['url'].split("?")[0]
    res2 = vkontakte_m3u8_downloader.parse_m3u8(res['url'])
    urllib.request.urlretrieve(f"{res2[len(res2)-1]}/index.m3u8", f"index{index}.m3u8")
    name = (res['artist'] + ' ' + res['title']).replace("'", "").replace('"', '')

    # convert m3u8 to broken mp3
    input = open(f"index{index}.m3u8", 'r')
    output = open(f"./music_vk/output{index}.mp3", 'wb')
    m3u82mp3.convert(input, output)

    # convert broken mp3 to normal mp3
    os.system(f"ffmpeg -i music_vk/output{index}.mp3 './music_vk/{name}.mp3' -y")

    # delete temp files
    os.system(f"rm index{index}.m3u8")
    os.system(f"rm music_vk/output{index}.mp3")

    return {name, os.path.abspath(f"./music_vk/{name}.mp3")}
