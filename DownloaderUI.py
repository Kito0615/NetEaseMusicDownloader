from NetEaseMusic import *

import tkinter as tk
from enum import Enum

url_type = Enum('url_type', ('url_type_playlist', 'url_type_album', 'url_type_mv', 'url_type_single'))

def default_ui():
	global window
	window = tk.Tk()
	window.title('Downloader')
	window.geometry('400x240')
	l = tk.Label(window, text='URL: ', font = ('Arial', 12), width = 14, height = 2)
	l.place(x=4, y=10)
	global e
	e = tk.Entry(window)
	e.place(x=66,y=11)
	b = tk.Button(window, text = 'Download', width = 10, height = 2, command = b_action)
	b.place(x=260,y=3)

	global ck_var
	ck_var = tk.IntVar()
	global l1
	l1 = tk.Label(window, text = 'Save to folder:%s'%(os.path.expanduser('~/Music/网易云音乐')), font=('Arial', 13), width = 50, height = 2)
	l1.place(x=-30,y=80)

	ck = tk.Checkbutton(window, text = 'Add to iTunes library ?', font = ('Arial', 13), variable = ck_var, onvalue = 1, offvalue = 0, command = ck_action)
	ck.place(x=30,y=50)

	window.mainloop()


def ck_action():
	var = ck_var.get()

def b_action():
	start_download()

def start_download():
	'''
	if judge_if_playlist(url):
		download_playlist(url, folder = folder)
	elif judge_if_album(url):
		download_album(url, folder = folder)
	elif judge_if_mv(url):
		download_mv(url, folder = folder)
	else:
		download_music(url, folder = folder)
	'''
	url = e.get()

	u_t = judge_url_type(url)

	if u_t == url_type.url_type_playlist:
		download_playlist(url)
	elif u_t == url_type.url_type_album:
		download_album(url)
	elif u_t == url_type.url_type_mv:
		download_mv(url)
	elif u_t == url_type.url_type_single:
		download_music(url)

def judge_url_type(url):
	if judge_if_playlist(url):
		return url_type.url_type_playlist
	elif judge_if_album(url):
		return url_type.url_type_album
	elif judge_if_mv(url):
		return url_type.url_type_mv
	return url_type.url_type_single

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

def main():
	default_ui()

if __name__ == '__main__':
	main()