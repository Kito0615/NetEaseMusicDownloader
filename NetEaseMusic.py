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
import os.path
import subprocess
import sys
import time
import getopt
import locale
from http import cookiejar as cj
import tempfile

# from requests import cookies
from config import http_error
from config import music_genre

from Crypto.Cipher import AES
import base64

__DATE__ = '2024-12-23'
__VERSION__ = 'V 0.7.4'

URL_TYPE_KEY = "url_type"
URL_TYPE_SINGLE = "single"
URL_TYPE_LIST = "playlist"
URL_TYPE_VIDEO = "video"
LIST_RANGE_KEY = "list_range"
ADD_TO_ITUNES_KEY = "add_to_itunes"
FOLDER_PATH_KEY = "folder_path"
COOKIE_FILE_KEY = "cookie_file"
URL_KEY = "url"


def _(s, lan='Chinese'):
    chineseStrings = {
        'Matching ID...': '匹配ID中...',
        'Obtain ID:': '取得ID: ',
        '❌ :Failed to get song details!': '❌ :获取歌曲详细信息失败！',
        '❌ :Failed to get MV details!': '❌ :获取音乐视频详细信息失败！',
        'Downloading song from official API...': '正在从官方接口下载歌曲...',
        'Downloading song from 3rd party API...': '正在从第三方接口下载歌曲...',
        '❌ :Response Error': '❌ :响应错误',
        'Downloading({}/{})': '下载中({}/{})',
        'Downloading【{}】{}/{}': '下载中《{}》 {}/{}',
        'Start parsing song list info...': '正在解析播放列表信息...',
        'Start parsing album info...': '正在解析专辑信息...',
        '❌ :Parsing of MV ID failed': '❌ :解析音乐视频ID失败',
        '❌ :Parsing of song or playlist ID failed': '❌ :解析歌曲/播放列表ID失败',
        'Downloading music:': '正在下载：',
        'Downloading Coverart:': '正在下载封面：',
        'Adding Coverart:': '正在添加封面：',
        'Searching on QQ Music...': '正在从搜索QQ音乐...',
        '❌ :Failed to download from QQ, you may need to pay for it separately.': '❌ :从QQ音乐下载失败，可能需要单独付费。',
        'Converting{origin} to {mp3}': '正在将{origin}转换成{mp3}格式',
        'Invalid download link.': '非法下载链接',
        'File already exists!': '文件已经存在！',
        'The coverart was applied successfully.': '已经成功添加封面。',
        'Song file was downloaded successfully.': '成功下载歌曲文件。',
        'Useage error.': '用法错误。',
        'output folder path : ': '输出目录：',
        'Module not found.': '模块未找到。',
        'Modules needed:requests, json, re, os, subprocess, sys': '需安装模块：requests, json, re, os, subprocess, sys',
        'Please use "pip3/pip install [module]" to install the corresponding module': '请使用"pip3/pip install [模块名]"来安装相应模块',
        'Type Error': '类型错误。',
        'Error Code :': '错误代码：'}
    if lan == 'Chinese':
        return chineseStrings[s]
    else:
        return s


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
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encrypt_text = encryptor.encrypt(text.encode('utf-8'))
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding='utf-8')
    return encrypt_text


def get_response(url, cookies=None):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    he = {"Referer": "http://music.163.com",
          'Host': 'music.163.com', 'User-Agent': ua,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    res = ''
    if cookies is not None:
        res = requests.get(url, headers=he, cookies=cookies)
    else :
        res = requests.get(url, headers=he)
    if res.status_code != 200:
        print('Network Error:', http_error[res.status_code])
        print(url)
    return json.loads(res.text)


def extract_id(input_url):
    print(_('Matching ID...'))
    match = re.search(r'id=\d{2,12}', input_url)
    if match:
        print(_('Obtain ID:'), match.group(0)[3:])
        return match.group(0)[3:]
    return None


def get_song_name_album_poster(type_id, cookie_file=''):
    api = f'http://music.163.com/api/song/detail?ids=[{type_id}]'
    json_obj = get_response(api)
    if not json_obj:
        print(_('❌ :Failed to get song details!'))
        return None
    print(f'Json : {json_obj}')
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
    ext = get_music_extension(song_obj)

    obj = Music(song_name, singers, album, year, track, poster, br, ext)
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

def get_music_extension(song_obj):
    ext = 'mp3'
    if 'hMusic' in song_obj and song_obj['hMusic'] is not None:
        br = song_obj['hMusic']['extension']
    elif 'mMusic' in song_obj and song_obj['mMusic'] is not None:
        br = song_obj['mMusic']['extension']
    elif 'lMusic' in song_obj and song_obj['lMusic'] is not None:
        br = song_obj['lMusic']['extension']
    elif 'bMusic' in song_obj and song_obj['bMusic'] is not None:
        br = song_obj['bMusic']['extension']

    return br


def get_max_size(size_keys):
    max_size = 0
    for key in size_keys:
        if int(key) > max_size:
            max_size = int(key)

    return str(max_size)


def get_mv_info(type_id, cookie_file=''):
    # api = 'https://api.imjad.cn/cloudmusic/?type=mv&id={}'.format(type_id)
    api = f'https://music.163.com/api/mv/detail?id={type_id}'
    requests_cookie = get_requests_cookie_from_file(cookie_file)
    json_obj = get_response(api, cookies=requests_cookie)
    if not json_obj:
        print(_('❌ :Failed to get MV details!'))
        return None

    mv_info = json_obj['data']
    size_keys = mv_info['brs'].keys()
    default_mv_url = mv_info['brs'][get_max_size(size_keys)]
    mv_name = mv_info['name']

    return (default_mv_url, mv_name)


def get_music_url_with_official_api(type_id, br, cookie_file=''):
    # This section is for test official encryption.
    print(_('Downloading song from official API...'))
    first_param = '{ids:"[%s]", br:"%s", csrf_token:""}' % (type_id, br)
    data = {'params': get_params(first_param).encode('utf-8'), 'encSecKey': get_encSecKey()}
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
    requests_cookie = get_requests_cookie_from_file(cookie_file)
    he = {"Referer": "http://music.163.com",
          'Host': 'music.163.com', 'User-Agent': ua,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    res = None
    try:
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        res = requests.post(url, headers=he, data=data, cookies=requests_cookie)
    except Exception as e:
        print(f'Exception occurred : {e}')
    d = json.loads(res.text)
    if d['code'] == 200:
        return d['data'][0]['url']
    return None

def get_playlist_songs(type_id, folder='', range='', cookie_file = ''):
    json_obj = get_playlist_info(type_id, cookie_file=cookie_file)
    if json_obj is None:
        print(_('❌ :Response Error'))
        return
    elif json_obj['code'] != 200:
        print(json_obj)
        return
    tracks = extract_playlist_ids(json_obj['result']['tracks'])
    idx = 1
    total = len(tracks)
    if len(range) == 0:
        for track in tracks:
            print(_('Downloading({}/{})').format(idx, total))
            url = f'http://music.163.com/#/song?id={track}'
            download_music(url, folder=folder)
            time.sleep(1)
            idx += 1
    else:
        for index in string_to_list(range):
            track = tracks[index - 1]
            print(_('Downloading({}/{})').format(index, len(tracks)))
            url = f'http://music.163.com/#/song?id={track}'
            download_music(url, folder=folder)
            time.sleep(1)


def get_album_songs(type_id, folder=''):
    # api = 'https://api.imjad.cn/cloudmusic/?type=album&id={}'.format(type_id)
    api = f'http://localhost:3000/album?id={type_id}'
    json_obj = get_response(api)
    if not json_obj:
        print(_('❌ :Response Error'))
        return

    tracks = extract_playlist_ids(json_obj['songs'])
    album_name = json_obj['album']['name']
    idx = 1
    total = len(tracks)

    for track in tracks:
        print(_('Downloading【{}】({}/{})' % (album_name, idx, total)))
        url = f'http://music.163.com/#/song?id={track}'
        download_music(url, folder)
        time.sleep(1)
        idx += 1


def extract_playlist_ids(tracks_json):
    ret_tracks = []
    for track in tracks_json:
        ret_tracks.append(track['id'])

    return ret_tracks


def download_playlist(url, folder='', range='', cookie_file=''):
    type_id = extract_id(url)
    print(_('Start parsing song list info...'))
    get_playlist_songs(type_id, folder=folder, range=range, cookie_file=cookie_file)


def download_album(url, folder='', cookie_file=''):
    type_id = extract_id(url)
    print(_('Start parsing album info...'))
    get_album_songs(type_id, folder=folder)


def download_mv(url, folder='', cookie_file=''):
    # pattern = https://music.163.com/#/mv?id={}
    print('Downloading MV...')
    type_id = extract_id(url)
    if not type_id:
        print(_('❌ :Parsing of MV ID failed'))
        return
    (mv_url, mv_name) = get_mv_info(type_id)
    download_file(mv_url, folder=folder, export_file_name=mv_name)


def download_music(url, folder='', cookie_file=''):
    # pattern = http://music.163.com/#/song?id={}
    if len(folder) > 0 and not os.path.exists(folder):
        os.mkdir(folder)
    type_id = extract_id(url)
    if not type_id:
        print(_('❌ :Parsing of song or playlist ID failed'))
        return

    music_obj = get_song_name_album_poster(type_id)
    if not music_obj.title:
        return

    print(_('Downloading music:'))
    url = get_music_url_with_official_api(type_id, music_obj.br, cookie_file)
    
    audio = download_file(url, cookie_file, folder=folder, export_file_name=music_obj.title, extension=music_obj.ext)

    if not audio:
        return
    print(_('Downloading Coverart:'))
    poster = download_file(music_obj.poster, cookie_file, folder=folder, export_file_name=music_obj.title)
    print(_('Adding Coverart:'))
    audio_name = ''
    if hasattr(audio, 'name'):
        audio_name = audio.name
    else:
        audio_name = audio
    add_poster(poster.name, music_obj.title, music_obj.artists,
               music_obj.album, music_obj.year, music_obj.track,
               audio_name, music_obj.br)


def convert_to_mp3(other_media):

    out_file = '.'.join(other_media.split('.')[:-1]) + '.mp3'

    print(_('Converting{origin} to {mp3}'.format(origin=other_media, mp3=out_file)))

    out_bytes = subprocess.check_output(['ffmpeg', '-i', other_media, '-c:a',
                                         'libmp3lame', '-aq', '2', out_file])
    print(out_bytes)

    return out_file

def get_requests_cookie_from_file(cookie_file=''):
    requests_cookie = requests.cookies.RequestsCookieJar()
    if (len(cookie_file) != 0) :
        if not os.path.isfile:
            return FileNotFoundError(f'Cookie file not found at: {cookie_file}')
        cookie = cj.MozillaCookieJar()
        try:
            cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
        except Exception as e:
            raise ValueError(f'Failed to load cookie text from {e}')
        for cookie_item in cookie:
            requests_cookie.set(
                name = cookie_item.name,
                value = cookie_item.value,
                domain = cookie_item.domain,
                path = cookie_item.path,
                rest = {'HttpOnly': cookie_item.get_nonstandard_attr('HttpOnly')}
            )
    return requests_cookie


def download_file(file_url, cookie_file='', folder='',
                  export_file_name=None, extension=None):

    if not file_url or len(file_url) == 0:
        print(_('Invalid download link.'))
        return None
    if not extension:
        extension = file_url.split('.')[-1].split('?')[0]

    if not export_file_name:
        export_file_name = file_url.split('/')[-1].split('?')[0]

    file = ''
    if len(folder) == 0:
        file = f'{export_file_name}.{extension}'
    else:
        file = folder + os.sep + export_file_name + '.' + extension

    if os.path.exists(file):
        print(_('File already exists!'))
        return file
    requests_cookie = get_requests_cookie_from_file(cookie_file)
    with requests.get(file_url, stream=True, cookies=requests_cookie) as response:
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
            print(_('The coverart was applied successfully.'))
        if remove_file(music):
            print(_('Song file was downloaded successfully.'))

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
    print('%s [-h|-l|-v|-s|-r|-a|-f|-c] [--help|--list|--video|--single|--range|--all|--folder|--cookies] url'
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
    print('\t-c, --cookies COOKIE.txt : Use cookies.txt to get VIP account info.')


def parse_option_values():
    opts, args = getopt.getopt(sys.argv[1:], 'hlsvr:af:c:',
                               ['help', 'list', 'single', 'video', 'range=', 'auto', 'folder=', 'cookies='])
    options = {ADD_TO_ITUNES_KEY: False, COOKIE_FILE_KEY: ''}
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
        if key in ('-c', '--cookies'):
            options[COOKIE_FILE_KEY] = value
    options[URL_KEY] = sys.argv[-1]
    return options


def main():
    global LANGUAGE
    loc = locale.getlocale()
    if loc[0] == 'zh_CN' or loc[0] == 'en_CN':
        LANGUAGE = 'Chinese'
    else:
        LANGUAGE = 'English'
    options = parse_option_values()
    if options[URL_KEY].startswith('http'):
        pass
    else:
        print(_('Useage error.'))
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
    print(_('output folder path : ') + output_folder)
    range_str = ''
    if LIST_RANGE_KEY in options:
        range_str = options[LIST_RANGE_KEY]

    if URL_TYPE_KEY in options:
        if options[URL_TYPE_KEY] == URL_TYPE_SINGLE:
            download_music(options[URL_KEY], folder=output_folder, cookie_file=options[COOKIE_FILE_KEY])
        elif options[URL_TYPE_KEY] == URL_TYPE_LIST:
            download_playlist(options[URL_KEY], folder=output_folder, range=range_str, cookie_file=options[COOKIE_FILE_KEY])
        elif options[URL_TYPE_KEY] == URL_TYPE_VIDEO:
            download_mv(options[URL_KEY], folder=output_folder, cookie_file=options[COOKIE_FILE_KEY])
    else:
        if judge_if_playlist(options[URL_KEY]):
            download_playlist(options[URL_KEY], folder=output_folder, range=range_str, cookie_file=options[COOKIE_FILE_KEY])
        elif judge_if_album(options[URL_KEY]):
            download_album(options[URL_KEY], folder=output_folder, cookie_file=options[COOKIE_FILE_KEY])
        elif judge_if_mv(options[URL_KEY]):
            download_mv(options[URL_KEY], folder=output_folder, cookie_file=options[COOKIE_FILE_KEY])
        else:
            download_music(options[URL_KEY], folder=output_folder, cookie_file=options[COOKIE_FILE_KEY])


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


def get_system_cache_folder():
    tempFolder = tempfile.gettempdir()
    return tempFolder


def playlist_id_analaysed(type_id):
    tempPath = get_system_cache_folder()
    tempFile = os.path.join(tempPath, str(type_id) + '.json')
    return tempFile


def get_playlist_info(type_id, cookie_file=''):
    tempFilePath = playlist_id_analaysed(type_id)
    if os.path.exists(tempFilePath):
        with open(tempFilePath, 'r') as file:
            json_obj = json.load(file)
            return json_obj
    else:
        api = f'https://music.163.com/api/playlist/detail?id={type_id}'
        # api = 'http://localhost:3000/playlist/detail?id={}'.format(type_id)
        requests_cookie = get_requests_cookie_from_file(cookie_file)
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
        he = {"Referer": "http://music.163.com",
            'Host': 'music.163.com', 'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        res = requests.get(api, headers=he, cookies=requests_cookie)
        json_obj = json.loads(res.text)
        if json_obj is not None and json_obj['code'] == 200:
            with open(tempFilePath, 'w') as f:
                json.dump(json_obj, f)
        return json_obj
    
class Music():
    def __init__(self, title, artists, album, year, track, poster, br, ext):
        self.title = title.replace('/', '_')
        self.artists = ','.join(artists)
        self.album = album
        self.year = year
        self.track = track
        self.poster = poster
        self.br = br
        self.ext = ext


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
        print(_('Module not found.'))
        print(_('Modules needed:requests, json, re, os, subprocess, sys'))
        print(_('Please use "pip3 install [module]" to install the corresponding module'))
        print(e)
    elif type(e) == TypeError:
        print(_('Type Error'))
        print(e)
    else:
        print(e)


def print_welcome():
    print('Welcome to Netease CloudMusic Downloader')
    print('\t1. This tool can download most of Netease Cloud Music songs,', end='')
    print('\t   except for separate payment songs (such as Taylor Swift)')
    print('\t2. You can download both songs and full playlists. Just paste the url correctly.')
    print('\t3. You can download a full playlists or just some songs from a playlist.')
    print('\t4. In order to get song with coverart and song info, remember to install lame.')
    print('\t   (you can download it on Homebrew or google it)', end='')
    print('\t resolution for MVs by default (TODO: Add MV resolution selection)')
    print('\t5. You can also download MVs and download the highest')
    print('\t6. Version:{}'.format(__VERSION__))
    print('\t7. Compilation date: {}'.format(__DATE__))
    print('\t8. Author: AnarL.(anar930906@gmail.com)')
    print('\t9. Translation: ignaciocastro(https://github.com/ignaciocastro)')
    print('\tNOTE: PLEASE APPLY TO YOUR CORRESPONDING COPYRIGHT LAWS IN YOUR COUNTRY.')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        if e:
            print(e)
