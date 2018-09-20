#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @author: AnarL. (anar930906@gmail.com)
# @environment: Python3 with requests
# @description: 使用本程序可以轻松下载网易云音乐的歌曲，只需要有歌曲的网页即可，单独付费歌曲无法下载。
#                本程序仅供学习交流使用，严禁用于任何商业用途，产生任何法律纠纷与作者无关。
#                 请尊重版权，树立版权意识。
# @README: 添加封面需要使用lame库，如果电脑中没有，请使用brew install lame或其他方式安装。暂时不支持在windows上运行
# @lisence: MIT


# Pyinstaller error
# solution:https://stackoverflow.com/questions/48876156/pyinstaller-fails-to-import-site-module-in-python3-on-macosx

import requests
import json
import re
import os
import subprocess
import sys
import time
import getopt
from config import http_error
from config import music_genre

from Crypto.Cipher import AES
import base64

__DATE__ = '2018年9月6日'
__VERSION__ = 'V 0.6.2'

URL_TYPE_KEY = "url_type"
URL_TYPE_SINGLE = "single"
URL_TYPE_LIST = "playlist"
URL_TYPE_VIDEO = "video"
LIST_RANGE_KEY = "list_range"
ADD_TO_ITUNES_KEY = "add_to_itunes"
FOLDER_PATH_KEY = "folder_path"
URL_KEY = "url"


def get_genre_code(genre):
    if genre in music_genre.keys():
        return music_genre[genre]
    return 13


def get_params(text):
    first_key = '0CoJUm6Qyw8W8jud'
    second_key = 'FFFFFFFFFFFFFFFF'
    h_encText = AES_encrypt(text, first_key)
    h_encText = AES_encrypt(h_encText, second_key)

    return h_encText


def get_encSecKey():
    encSecKey = ('257348aecb5e556c066de214e5'
                 '31faadd1c55d814f9be95fd06d6bf'
                 'f9f4c7a41f831f6394d5a3fd2e388'
                 '1736d94a02ca919d952872e7d0a50e'
                 'bfa1769a7a62d512f5f1ca21aec60b'
                 'c3819a9c3ffca5eca9a0dba6d6f7249'
                 'b06f5965ecfff3695b54e1c28f3f624'
                 '750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c')
    return encSecKey


def AES_encrypt(text, key):
    iv = '0102030405060708'
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding='utf-8')
    return encrypt_text


def get_response(url):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
    res = requests.get(url, headers={'User-Agent': ua})
    if res.status_code != 200:
        print('Network Error:', http_error[res.status_code])
        print(url)
    return json.loads(res.text)


def extract_id(input_url):
    print('Matching ID...')
    match = re.search(r'id=\d{2,12}', input_url)
    if match:
        print('Obtain ID：', match.group(0)[3:])
        return match.group(0)[3:]
    return None


def get_song_name_album_poster(type_id):
    api = 'http://music.163.com/api/song/detail?ids=[{}]'.format(type_id)
    json_obj = get_response(api)
    if not json_obj:
        print('❌：Failed to get song details！')
        return None

    song_obj = json_obj['songs'][0]
    song_name = song_obj['name']
    artists = song_obj['artists']
    singers = []
    for ar in artists:
        singers.append(ar['name'])

    album_obj = None
    if 'al' in song_obj.keys():
        album_obj = song_obj['al']
    elif 'album' in song_obj.keys():
        album_obj = song_obj['album']
    album = album_obj['name']
    year = year_of_timestamp(album_obj['publishTime'] / 1000)
    track = song_obj['no']
    poster = album_obj['picUrl']
    br = get_music_best_bitrate(song_obj)

    obj = Music(song_name, singers, album, year, track, poster, br)
    return obj


def get_music_best_bitrate(song_obj):
    br = 96000
    if 'hMusic' in song_obj and song_obj['hMusic'] is not None:
        br = song_obj['hMusic']['bitrate']
    elif 'mMusic' in song_obj and song_obj['mMusic'] is not None:
        br = song_obj['mMusic']['bitrate']
    elif 'lMusic' in song_obj and song_obj['lMusic'] is not None:
        br = song_obj['lMusic']['bitrate']
    elif 'bMusic' in song_obj and song_obj['bMusic'] is not None:
        br = song_obj['bMusic']['bitrate']

    return br


def get_max_size(size_keys):
    max_size = 0
    for key in size_keys:
        if int(key) > max_size:
            max_size = int(key)

    return str(max_size)


def get_mv_info(type_id):
    api = 'https://api.imjad.cn/cloudmusic/?type=mv&id={}'.format(type_id)
    json_obj = get_response(api)
    if not json_obj:
        print('❌ :Failed to get MV details!')
        return None

    mv_info = json_obj['data']
    size_keys = mv_info['brs'].keys()
    default_mv_url = mv_info['brs'][get_max_size(size_keys)]
    mv_name = mv_info['name']

    return (default_mv_url, mv_name)


def get_music_url_with_official_api(type_id, br):
    # This section is for test official encryption.
    print('Downloading song from official API...')
    first_param = '{ids:"[%s]", br:"%s", csrf_token:""}' % (type_id, br)
    data = {'params': get_params(first_param).encode('utf-8'), 'encSecKey': get_encSecKey()}
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
    he = {"Referer": "http://music.163.com",
          'Host': 'music.163.com', 'User-Agent': ua,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    res = None
    try:
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        res = requests.post(url, headers=he, data=data)
    except Exception as e:
        print(e)
    #
    d = json.loads(res.text)
    if d['code'] == 200:
        return d['data'][0]['url']
    return None


def get_music_url_with_3rd_party_api(type_id, br):
    print('Downloading song from 3rd party API...')
    api = 'https://api.imjad.cn/cloudmusic?type=song&id={}&br={}'.format(type_id, br)
    json_obj = get_response(api)
    if not json_obj:
        print('❌ :Response Error')
        return None
    return json_obj['data'][0]['url']


def get_playlist_songs(type_id, folder='', range=''):
    api = 'http://music.163.com/api/playlist/detail?id={}'.format(type_id)
    json_obj = get_response(api)
    if not json_obj:
        print('❌：Response Error')
        return
    tracks = extract_playlist_ids(json_obj['result']['tracks'])
    # print(tracks)
    idx = 1
    total = len(tracks)
    if len(range) == 0:
        for track in tracks:
            print('Downloading({}/{})'.format(idx, total))
            url = 'http://music.163.com/#/song?id={}'.format(track)
            download_music(url, folder=folder)
            time.sleep(1)
            idx += 1
    else:
        for index in string_to_list(range):
            track = tracks[index - 1]
            print('Downloading({}/{})'.format(index, len(tracks)))
            url = 'http://music.163.com/#/song?id={}'.format(track)
            download_music(url, folder=folder)
            time.sleep(1)


def get_album_songs(type_id, folder=''):
    api = 'https://api.imjad.cn/cloudmusic/?type=album&id={}'.format(type_id)
    json_obj = get_response(api)
    if not json_obj:
        print('❌：Response Error')
        return

    tracks = extract_playlist_ids(json_obj['songs'])
    album_name = json_obj['album']['name']
    idx = 1
    total = len(tracks)

    for track in tracks:
        print('Downloading《{}》({}/{})'.format(album_name, idx, total))
        url = 'http://music.163.com/#/song?id={}'.format(track)
        download_music(url, folder)
        time.sleep(1)
        idx += 1


def extract_playlist_ids(tracks_json):
    ret_tracks = []
    for track in tracks_json:
        ret_tracks.append(track['id'])

    return ret_tracks


def download_playlist(url, folder='', range=''):
    type_id = extract_id(url)
    print('Start parsing song list info...')
    get_playlist_songs(type_id, folder=folder, range=range)


def download_album(url, folder=''):
    type_id = extract_id(url)
    print('Start parsing album info...')
    get_album_songs(type_id, folder=folder)


def download_mv(url, folder=''):
    # pattern = https://music.163.com/#/mv?id={}
    print('Downloading MV...')
    type_id = extract_id(url)
    if not type_id:
        print('❌ :Parsing of MV ID failed')
        return
    (mv_url, mv_name) = get_mv_info(type_id)
    download_file(mv_url, folder=folder, export_file_name=mv_name)


def download_music(url, folder=''):
    # pattern = http://music.163.com/#/song?id={}
    if len(folder) > 0 and not os.path.exists(folder):
        os.mkdir(folder)
    type_id = extract_id(url)
    if not type_id:
        print('❌ :Parsing of song or playlist ID failed')
        return

    music_obj = get_song_name_album_poster(type_id)
    if not music_obj.title:
        return

    print('Downloading music:')
    url = get_music_url_with_official_api(type_id, music_obj.br)
    if url is None:
        url = get_music_url_with_3rd_party_api(type_id, music_obj.br)

    audio = download_file(url, folder=folder, export_file_name=music_obj.title)
    print('------>')
    if not audio:
        audio = try_get_file_in_qq_music(music_obj.title, music_obj.artists)

    if not audio:
        return
    print('Downloading Coverart:')
    poster = download_file(music_obj.poster, folder=folder, export_file_name=music_obj.title)
    print('Adding Coverart:')
    audio_name = ''
    if hasattr(audio, 'name'):
        audio_name = audio.name
    else:
        audio_name = audio
    add_poster(poster.name, music_obj.title, music_obj.artists,
               music_obj.album, music_obj.year, music_obj.track,
               audio_name, music_obj.br)


QQ_music_search_tip_api = ('https://c.y.qq.com/soso/fcgi-bin'
                           '/client_search_cp?ct=24&qqmusic_ver=1298'
                           '&new_json=1&remoteplace=txt.yqq.song'
                           '&searchid=56069080114511262&t=0'
                           '&aggr=1&cr=1&catZhida=1&lossless=0'
                           '&flag_qc=0&p={page}&n=20&w={song_name}'
                           '&g_tk=5381&loginUin=0&hostUin=0'
                           '&format=json&inCharset=utf8'
                           '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0')
QQ_music_song_info_api = ('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
                          '?g_tk=63395543&hostUin=0&format=json&inCharset=utf8'
                          '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
                          '&cid=205361747&songmid={song_id}'
                          '&filename=C400{song_id}.m4a&guid=9362313912')
QQ_music_song_dl_api = ('http://dl.stream.qqmusic.qq.com'
                        '/{file_name}?vkey={v_key}&guid=9362313912'
                        '&uin=0&fromtag=66')


def search_qq_music(music_name, singer):

    print('Searching on QQ Music...')
    url = QQ_music_search_tip_api.format(page=1, song_name=music_name)
    json_obj = get_response(url)
    songs = json_obj['data']['song']['list']

    target_id = ''

    for item in songs:
        item_singer = item['singer'][0]['name']

        if item_singer == singer:
            target_id = item['mid']
            break

    return target_id


def get_qq_music_dl_info(mid):
    url = QQ_music_song_info_api.format(song_id=mid)
    json_obj = get_response(url)

    song_obj = json_obj['data']['items'][0]
    return (song_obj['vkey'], song_obj['filename'])


def download_qq_music(song_vkey, song_title, song_file_name):
    url = QQ_music_song_dl_api.format(file_name=song_file_name,
                                      v_key=song_vkey)
    if len(song_vkey) == 0:
        print('❌ :Failed to download from QQ, you may need to pay for it separately.')
        return ""
    ext = song_file_name.split('.')[-1]
    file_name = '.'.join([song_title, ext])
    res = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(res.content)

    return file_name


def convert_to_mp3(other_media):

    out_file = '.'.join(other_media.split('.')[:-1]) + '.mp3'

    print('Converting{origin} to {mp3}'.format(origin=other_media, mp3=out_file))

    out_bytes = subprocess.check_output(['ffmpeg', '-i', other_media, '-c:a',
                                         'libmp3lame', '-aq', '2', out_file])
    print(out_bytes)

    return out_file


def try_get_file_in_qq_music(song_name, singer):
    print('Searching on QQ Music...')
    try:
        music_id = search_qq_music(song_name, singer)
        (song_v_key, song_file_name) = get_qq_music_dl_info(music_id)
        song_file = download_qq_music(song_v_key, song_name, song_file_name)
        mp3_file = ''

        if len(song_file) == 0:
            return None

        if song_file.split('.')[-1] != 'mp3':
            mp3_file = convert_to_mp3(song_file)
            os.remove(song_file)

        return mp3_file
    except Exception as e:
        print(e)


def download_file(file_url, folder='',
                  export_file_name=None, extension=None):

    if not file_url or len(file_url) == 0:
        print('Invalid download link.')
        return None
    if not extension:
        extension = file_url.split('.')[-1]

    if not export_file_name:
        export_file_name = file_url.split('/')[-1]

    file = ''
    if len(folder) == 0:
        file = export_file_name + '.' + extension
    else:
        file = folder + os.sep + export_file_name + '.' + extension

    if os.path.exists(file):
        print('File already exists！')
        return file
    with requests.get(file_url, stream=True) as response:
        #  单次请求最大值
        chunk_size = 1024
        #  内容总体大小
        content_size = int(response.headers['content-length'])
        progress = ProgressBar(export_file_name + '.' + extension,
                               total=content_size, unit='kb',
                               chunk_size=chunk_size,
                               run_status='Downloading', fin_status='Download completed')

        with open(file, 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))

    return file


def install_lame():
    ret = subprocess.check_output(['brew', 'install', 'lame'])
    print(ret)


def add_poster(poster, title, artists, album, year, track, music, br):
    ret = os.system('lame --version')
    if ret != 0:
        install_lame()
    try:
        params = ['lame', '--tt', title, '--ta', artists,
                  '--tl', album, '--ty', str(year), '--tc', str(track),
                  '--tg', '13', '--ti', poster, '-b', str(br), music]
        out_bytes = subprocess.check_output(params)
        print(out_bytes.decode('utf-8'))
        if remove_file(poster):
            print('The coverart was applied successfully。')
        if remove_file(music):
            print('Song file was downloaded successfully。')

        old_file = music + '.' + music.split('.')[-1]
        if os.path.exists(old_file):
            os.rename(old_file, music)

    except Exception as e:
        print(e)


def remove_file(file):
    if os.path.exists(file):
        os.remove(file)
        return True
    return False


def string_to_list(s):
    result = []
    for part in s.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)
    return result


def get_itunes_library_path():
    itunes_path = ('~/Music/iTunes/iTunes Media/'
                   'Automatically Add to iTunes')
    path = os.path.expanduser(itunes_path)
    ext = os.path.exists(path)
    if not ext:
        itunes_path = ('~/Music/iTunes/iTunes Media/'
                       'Automatically Add to iTunes.localized/')
    return os.path.expanduser(itunes_path)


def show_usage():
    print('%s [-h|-l|-v|-s|-r|-a|-f] [--help|--list|--video|--single|--range|--all|--folder] url'
          % (__file__))
    print('Usage :')
    print('\t-h, --help           : show this help message.')
    print('\t-s, --single         : means the url will download is a single url.')
    print('\t                       if not use this option, script will judge automatically.')
    print('\t-l, --list           : means the url will download is a playlist url.')
    print('\t                       if not use this option, script will judge automatically.')
    print('\t-v, --video          : means the url will download is a music video url.')
    print('\t                       if not use this option, script will judge automatically.')
    print('\t-r, --range RANGE    : download the playlist in RANGE.')
    print('\t                       RANGE supported format [start:end], [start:], [:end],')
    print('\t                       starts with 1, ends with length of list.')
    print('\t                       if not use this option, script will download all')
    print('\t                       automatically.')
    print('\t-a, --auto           : use this option to add download media to')
    print('\t                       iTunes library automatically.')
    print('\t                       if not use this option, script will donwload media to the')
    print('\t                       FOLDER with -f|--folder option or the current directory if')
    print('\t                       not use -f|--folder option too.')
    print('\t-f, --folder FOLDER  : save downloaded media to FOLDER')
    print('\t                       if not use this option, script will download media to the')
    print('\t                       current directory or iTunes library path if -a|--auto used.')


def parse_option_values():
    opts, args = getopt.getopt(sys.argv[1:], 'hlsvr:af:',
                               ['help', 'list', 'single', 'video', 'range=', 'auto', 'folder='])
    options = {ADD_TO_ITUNES_KEY: False}
    for key, value in opts:
        if key in ('-h', '--help'):
            show_usage()
            sys.exit(0)
        if key in ('-s', '--single'):
            options[URL_TYPE_KEY] = URL_TYPE_SINGLE
        if key in ('-l', '--list'):
            options[URL_TYPE_KEY] = URL_TYPE_LIST
        if key in ('-v', '--video'):
            options[URL_TYPE_KEY] = URL_TYPE_VIDEO
        if key in ('-a', '--auto'):
            options[ADD_TO_ITUNES_KEY] = True
        if key in ('-r', '--range'):
            options[LIST_RANGE_KEY] = value
        if key in ('-f', '--folder'):
            options[FOLDER_PATH_KEY] = value
    options[URL_KEY] = sys.argv[-1]
    return options


def main():
    options = parse_option_values()
    if options[URL_KEY].startswith('http'):
        pass
    else:
        print('Useage error.')
        show_usage()
        sys.exit(-1)
    print_welcome()
    output_folder = ''
    if options[ADD_TO_ITUNES_KEY]:
        output_folder = get_itunes_library_path()
    elif FOLDER_PATH_KEY in options:
        output_folder = os.path.expanduser(options[FOLDER_PATH_KEY])
    else:
        output_folder = os.getcwd()
    print('output folder path : ' + output_folder)
    range_str = ''
    if LIST_RANGE_KEY in options:
        range_str = options[LIST_RANGE_KEY]

    if URL_TYPE_KEY in options:
        if options[URL_TYPE_KEY] == URL_TYPE_SINGLE:
            download_music(options[URL_KEY], folder=output_folder)
        elif options[URL_TYPE_KEY] == URL_TYPE_LIST:
            download_playlist(options[URL_KEY], folder=output_folder, range=range_str)
        elif options[URL_TYPE_KEY] == URL_TYPE_VIDEO:
            download_mv(options[URL_KEY], folder=output_folder)
    else:
        if judge_if_playlist(options[URL_KEY]):
            download_playlist(options[URL_KEY], folder=output_folder, range=range_str)
        elif judge_if_album(options[URL_KEY]):
            download_album(options[URL_KEY], folder=output_folder)
        elif judge_if_mv(options[URL_KEY]):
            download_mv(options[URL_KEY], folder=output_folder)
        else:
            download_music(options[URL_KEY], folder=output_folder)


def judge_if_playlist(url):
    if url.find('playlist') != -1:
        return True
    return False


def judge_if_album(url):
    if url.find('album') != -1:
        return True
    return False


def judge_if_mv(url):
    if url.find('mv') != -1:
        return True
    return False


def year_of_timestamp(unix_time):
    return time.localtime(unix_time)[0]


class Music():
    def __init__(self, title, artists, album, year, track, poster, br):
        self.title = title
        self.artists = ','.join(artists)
        self.album = album
        self.year = year
        self.track = track
        self.poster = poster
        self.br = br


class ProgressBar(object):
    def __init__(self, title, count=0.0,
                 run_status=None, fin_status=None,
                 total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = '【%s】%s %.2f %s %s %.2f %s'
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ''
        self.fin_status = fin_status or ' ' * len(self.status)
        self.unit = unit
        self.sep = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size,
                             self.unit, self.sep,
                             self.total / self.chunk_size,
                             self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = '\r'
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def print_exception_solution(e):
    if type(e) == ModuleNotFoundError:
        print('Module not found.')
        print('Modules needed:requests, json, re, os, subprocess, sys')
        print('Please use "pip3 install [module]" to install the corresponding module')
        print(e)
    elif type(e) == TypeError:
        print('Type Error')
        print(e)
    else:
        print(e)


def print_welcome():
    print('Welcome to Netease CloudMusic Downloader')
    print('1. This tool can download most of Netease Cloud Music songs, except for separate payment songs (such as Taylor Swift)')
    print('2. You can download both songs and full playlists. Just paste the url correctly.')
    print('3. You can download a full playlists or just some songs from a playlist.')
    print('4. In order to get song with coverart and song info, remember to install lame. (you can download it on Homebrew or google it)')
    print('5. You can also download MVs and download the highest resolution for MVs by default (TODO: Increase MV resolution)')
    print('6. Shortcut: NetEaseMusic [url] [folder]')
    print('7. Version:{}'.format(__VERSION__))
    print('8. Compilation date: {}'.format(__DATE__))
    print('9. Author: AnarL.(anar930906@gmail.com)')
    print('10. Translation: ignaciocastro')
    print('NOTE: PLEASE APPLY TO YOUR CORRESPONDING COPYRIGHT LAWS IN YOUR COUNTRY.\t\t\t\t\t\t\t\t*')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        if e:
            print(e)
