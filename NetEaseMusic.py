#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @author: AnarL. (anar930906@gmail.com)
# @version: V0.3.1
# @environment: Python3
# @description: 使用本程序可以轻松下载网易云音乐的歌曲，只需要有歌曲的网页即可，单独付费歌曲无法下载。
#				本程序仅供学习交流使用，严禁用于任何商业用途，产生任何法律纠纷与作者无关。
# 				请尊重版权，树立版权意识。
# @README: 添加封面需要使用lame库，如果电脑中没有，请使用brew install lame或其他方式安装。暂时不支持在windows上运行
# @lisence: MIT


# //Pyinstaller error solution:https://stackoverflow.com/questions/48876156/pyinstaller-fails-to-import-site-module-in-python3-on-macosx

import requests, json, re, os
import subprocess, sys, time, datetime

http_error = {
	400 : '请求错误',
	401 : '未授权',
	402 : '要求付费',
	403 : '服务器禁止',
	404 : '无法找到文件',
	405 : '资源被禁止',
	406 : '无法接受请求',
	407 : '要求代理身份验证',
	408 : '请求超时',
	409 : '请求冲突',
	410 : '永远不可用',
	411 : '要求的长度',
	412 : '先决条件失败',
	413 : '请求实例太长',
	414 : '请求url太长',
	415 : '不支持的媒体类型',
	416 : '无法满足的请求范围',
	417 : '失败的预期',
	500 : '内部服务器错误',
	501 : '未实现',
	502 : '网关错误',
	503 : '不可用的服务',
	504 : '网关超时',
	505 : 'HTTP版本未被支持'

}

def get_response(url):
	res = requests.get(url, headers = {'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'})
	if res.status_code != 200:
		print('Error:', http_error[res.status_code])
	return json.loads(res.text)

def extract_id(input_url):
	print('匹配ID...')
	match = re.search('id=\d{2,12}', input_url)
	if match:
		print('取得ID：', match.group(0)[3:])
		return match.group(0)[3:]
	return None

def get_song_name_album_poster(type_id):
	api = 'https://api.imjad.cn/cloudmusic/?type=detail&id={}'.format(type_id)
	json_obj = get_response(api)
	if not json_obj:
		print('❌：获取歌曲详细信息失败！')
		return None

	song_obj = json_obj['songs'][0]
	song_name = song_obj['name']
	artists = song_obj['ar']
	singers = []
	for ar in artists:
		singers.append(ar['name'])
	album = song_obj['al']['name']
	year = year_of_timestamp(song_obj['publishTime'] / 1000)
	track = song_obj['no']
	poster = song_obj['al']['picUrl']

	obj = Music(song_name, singers, album, year, track, poster)
	return obj

def get_playlist_songs(type_id, folder = ''):
	api = 'http://music.163.com/api/playlist/detail?id={}'.format(type_id)
	json_obj = get_response(api)
	if not json_obj:
		print('❌：响应错误')
		return
	tracks = extract_playlist_ids(json_obj['result']['tracks'])
	# print(tracks)
	idx = 1
	total = len(tracks)
	for track in tracks:
		print('正在下载({}/{})'.format(idx, total))
		url = 'http://music.163.com/#/song?id={}'.format(track)
		download_music(url, folder = folder)
		time.sleep(1)
		idx += 1


def extract_playlist_ids(tracks_json):
	ret_tracks = []
	for track in tracks_json:
		ret_tracks.append(track['id'])

	return ret_tracks

def download_playlist(url, folder = ''):
	type_id = extract_id(url)
	print('开始解析播放列表信息...')
	get_playlist_songs(type_id, folder = folder)


def download_music(url, folder = ''):
	# pattern = http://music.163.com/#/song?id={}
	if len(folder) > 0 and not os.path.exists(folder):
		os.mkdir(folder)
	type_id = extract_id(url)
	if not type_id:
		print('❌ :解析歌曲或播放列表ID失败')
		return
	music_obj = get_song_name_album_poster(type_id)
	if not music_obj.title:
		return

	api = 'https://api.imjad.cn/cloudmusic?type=song&id={}&br=320000'.format(type_id)
	json_obj = get_response(api)
	if not json_obj:
		print('❌ :响应错误')
		return
	print('开始下载音乐:')
	audio = download_file(json_obj['data'][0]['url'],folder = folder,  export_file_name = music_obj.title)
	print('------>')
	if not audio:
		audio = try_get_file_in_qq_music(music_obj.title, music_obj.artists)

	if not audio:
		return
	print('开始下载封面:')
	poster = download_file(music_obj.poster, folder = folder,  export_file_name = music_obj.title)
	print('开始添加封面:')
	audio_name = ''
	if hasattr(audio, 'name'):
		audio_name = audio.name
	else :
		audio_name = audio
	add_poster(poster.name, music_obj.title, music_obj.artists, music_obj.album, music_obj.year, music_obj.track, audio_name)


QQ_music_search_tip_api = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=56069080114511262&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p={page}&n=20&w={song_name}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
QQ_music_song_info_api = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=63395543&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&songmid={song_id}&filename=C400{song_id}.m4a&guid=9362313912'
QQ_music_song_dl_api = 'http://dl.stream.qqmusic.qq.com/{file_name}?vkey={v_key}&guid=9362313912&uin=0&fromtag=66'

def search_qq_music(music_name, singer):

	print('search in qq music...')
	url = QQ_music_search_tip_api.format(page = 1, song_name = music_name)
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
	url = QQ_music_song_info_api.format(song_id = mid)
	json_obj = get_response(url)

	song_obj = json_obj['data']['items'][0]
	return (song_obj['vkey'], song_obj['filename'])

def download_qq_music(song_vkey, song_title, song_file_name):
	url = QQ_music_song_dl_api.format(file_name = song_file_name, v_key = song_vkey)
	print(song_file_name)
	ext = song_file_name.split('.')[-1]
	file_name = '.'.join([song_title, ext])
	res = requests.get(url)
	with open(file_name, 'wb') as f:
		f.write(res.content)

	return file_name

def convert_to_mp3(other_media):

	out_file = '.'.join(other_media.split('.')[:-1]) + '.mp3'

	print('converting {origin} to {mp3}'.format(origin = other_media, mp3 = out_file))

	out_bytes = subprocess.check_output(['ffmpeg', '-i', other_media, '-c:a', 'libmp3lame', '-aq', '2', out_file])
	print(out_bytes)

	return out_file


def try_get_file_in_qq_music(song_name, singer):
	print('try to search in qq music.')
	music_id = search_qq_music(song_name, singer)
	(song_v_key, song_file_name) = get_qq_music_dl_info(music_id)
	song_file = download_qq_music(song_v_key, song_name, song_file_name)
	mp3_file = ''

	if song_file.split('.')[-1] != 'mp3':
		mp3_file = convert_to_mp3(song_file)
		os.remove(song_file)

	return mp3_file


def download_file(file_url, folder = '', export_file_name = None, extension = None):

	if not file_url or len(file_url) == 0:
		print('下载链接无效.')
		return None
	if not extension:
		extension = file_url.split('.')[-1]

	if not export_file_name:
		export_file_name = file_url.split('/')[-1]

	file = ''
	if len(folder) == 0:
		file = export_file_name + '.' + extension
	else :
		file = folder + os.sep + export_file_name + '.' + extension

	if os.path.exists(file):
		print('文件已存在！')
		return
	with requests.get(file_url, stream = True) as response:
		chunk_size = 1024 # 单次请求最大值
		content_size = int(response.headers['content-length']) #内容总体大小
		progress = ProgressBar(export_file_name + '.' + extension, total = content_size, unit = 'kb', chunk_size = chunk_size, run_status = '正在下载', fin_status = '下载完成')

		with open(file, 'wb') as file:
			for data in response.iter_content(chunk_size = chunk_size):
				file.write(data)
				progress.refresh(count = len(data))

	return file

def install_lame():
	ret = subprocess.check_output(['brew', 'install', 'lame'])
	print(ret)


def add_poster(poster, title, artists, album, year, track, music):
	ret = os.system('lame --version')
	if ret != 0:
		install_lame()
		
	try:
		out_bytes = subprocess.check_output(['lame', '--tt', title, '--ta', artists, '--tl', album, '--ty', str(year), '--tc', str(track), '--tg', '13', '--ti', poster, '-b', '320000', music])
		print(out_bytes.decode('utf-8'))
		if remove_file(poster):
			print('删除封面文件成功。')
		if remove_file(music):
			print('删除音乐文件成功。')

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

def main():
	url = ''
	folder = ''
	if len(sys.argv) == 1:
		url = input('请输入/粘贴歌曲网页地址.\n地址:')
	elif len(sys.argv) == 2:
		url = sys.argv[1]
	elif len(sys.argv) == 3:
		url = sys.argv[1]
		folder = sys.argv[2]

	if not judge_if_playlist(url):
		download_music(url, folder = folder)
		return
	download_playlist(url, folder = folder)


def judge_if_playlist(url):
	if url.find('playlist') != -1:
		return True
	return False

def year_of_timestamp(unix_time):
	return time.localtime(unix_time)[0]

class Music():
	def __init__(self, title, artists, album, year, track, poster):
		self.title = title
		self.artists = ','.join(artists)
		self.album = album
		self.year = year
		self.track = track
		self.poster = poster

class ProgressBar(object):
	def __init__(self, title, count = 0.0, run_status = None, fin_status = None, total = 100.0, unit = '', sep = '/', chunk_size = 1.0):
		super(ProgressBar, self).__init__()
		self.info = '【%s】%s %.2f %s %s %.2f %s'
		self.title = title
		self.total = total
		self.count = count
		self.chunk_size = chunk_size
		self.status = run_status or ''
		self.fin_status = fin_status or ' '*len(self.status)
		self.unit = unit
		self.sep = sep


	def __get_info(self):
		# 【名称】状态 进度 单位 分割线 总数 单位
		_info = self.info%(self.title, self.status, self.count / self.chunk_size, self.unit, self.sep, self.total / self.chunk_size, self.unit)
		return _info

	def refresh(self, count = 1, status = None):
		self.count += count
		# if status is not None:
		self.status = status or self.status
		end_str = '\r'
		if self.count >= self.total:
			end_str = '\n'
			self.status = status or self.fin_status
		print(self.__get_info(), end = end_str)

def print_exception_solution(e):
	if type(e) == ModuleNotFoundError:
		print('没有找到对应模块.')
		print('本程序引用模块:requests, json, re, os, subprocess, sys')
		print('请使用"pip3 install [模块]" 安装对应模块')
		print(e)
	elif type(e) == TypeError:
		print('类型错误')
		print(e)
	else:
		print(e)

def print_welcome():
	print('*'*97)
	print('*\t\t\t\t欢迎使用网易云音乐下载工具\t\t\t\t\t*')
	print('*'*97)
	print('* 1.本工具可以下载网易云音乐收费歌曲(单独付费除外，如霉霉的歌曲。)\t\t\t\t*')
	print('* 2.可以下载单曲，也可以下载播放列表，只需要复制单曲或播放列表的网页地址即可。\t\t\t*')
	print('* 3.可以专辑封面，但是需要电脑有lame库。如果没有，可以自动安装(需要系统有包管理工具Homebrew)\t*')
	print('* 4.快捷方式:NetEaseMusic [url] [folder] //表示将连接url对应的文件下载到指定目录folder\t\t*')
	print('* 5.版本:V 0.3.1\t\t\t\t\t\t\t\t\t\t*')
	print('* 6.编译日期: 2018年5月17日\t\t\t\t\t\t\t\t\t*')
	print('* 7.作者: AnarL.(anar930906@gmail.com)\t\t\t\t\t\t\t\t*')
	print('*'*97)
	print('* *注:请尊重版权，树立版权意识。\t\t\t\t\t\t\t\t*')
	print('*'*97)

if __name__ == '__main__':
	try:
		print_welcome()
		main()
	except Exception as e:
		if e :
			print(e)