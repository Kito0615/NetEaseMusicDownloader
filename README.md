# NetEaseMusicDownloader

[中文说明](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/README_CN.md)

![](https://img.shields.io/badge/Platform-Python3-009eff.svg) ![](https://img.shields.io/badge/Windows-Supported-00efff.svg)  ![](https://img.shields.io/badge/MacOS-Supported-00efff.svg) ![](https://img.shields.io/badge/Linux-Supported-00efff.svg) ![](https://img.shields.io/badge/WebAPI-Available-00efff.svg)

> **NOTE:** In this script, I used some api via [AD&#39;s API](https://api.imjad.cn/). Thanks. This
> script is for personal use only. It cannot be used for any commercial
> activities. All legal issues are not related to the author.
>
> **NOTE**: **Third part API server is outdated. Now this project will not be useful. If you want to use this project, you can check this [NetEaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) project and modify api requests in this project.**

#### Update:2024-12-23

1. Added cache to reduce presure for official server.
2. Fixed `Playst` and `Music Video` cannot download.
3. Fixed other issues. 

#### Update:2024-12-16

1. Remove search source from [QQMusic](https://y.qq.com).
2. Add new feature for VIP user use cookie file to download with VIP permission.
3. Other update.

#### Update: 2019-06-6

1. Fix code.
2. Localization

#### Update:2018-09-06

1. **New version of Downloader.**Add some options for the script.
2. Usage : `python3 NetEaseMusic.py ` `[OPTIONS]` `URL` or `NetEaseMusic`  `[OPTIONS]` `URL`
3. Option List:

   | Option            | Instruction                              |
   | ----------------- | ---------------------------------------- |
   | -h, --help        | Show help message.                       |
   | -s, --single      | Specific the URL is a single music.      |
   | -l, --list        | Specific the URL is a list.              |
   | -v, --video       | Specific the URL is a music video.       |
   | -r, --range RANGE | Specific to download the music in RANGE. |
   |                   | RANGE format like '1, 2, 5-7, 18'        |
   | -a, --auto        | Add to iTunes Library automatically.     |
   | -f, --folder      | Specific the destination folder.         |

#### Update:2018-08-09

1. Add Lame Tag for iTunes.
2. Now offcial web api failed, still using thrid-part API from AD. I will fix this ASAP.

#### Update: 2018-07-17

1. Add API from official website crack.
2. Add song best bit rate detect.

#### Update: 2018-06-14

1. Add ask for "Add to iTunes automatically".
2. Fixed break down when file exists or search in QQMusic failed.

#### Update:2018-05-28

1. Use new non-offcial api which get from the web replaced the old api.

#### Update:2018-05-22:

1. Now you can use this tool to download songs/playlists/albums. Use *AD's API*.
2. Support windows now.
3. Support NetEaseMusic MV download now.

#### Update:2018-05-17

1. Add new source from [QQMusic](http://y.qq.com) when the song not available with [NetEaseMusic](http://music.163.com).
2. Add new dependencies [FFMPEG](http://ffmpeg.org) for convert source from QQMusic with *.m4a* extension to *.mp3*.

#### Download:

1. **Clone project**

   ```shell
   git clone https://github.com/Kito0615/NetEaseMusic.git
   ```

   Then you can run script(NetEaseMusic.py) in terminal with python3. Like:

   ```shell
   python3 NetEaseMusic.py
   ```

   or:

   ```shell
   chmod +x NetEaseMusic.py
   ./NetEaseMusic.py
   ```
2. **Download release**

   Click [here](https://github.com/Kito0615/NetEaseMusicDownloader/releases), download the version you need. Then you can run the binary file in terminal like:

   ```shell
   ./NetEaseMusic
   ```

   or copy the binary to `/usr/local/bin`, then you can execute the binary anywhere you want.

   ```shell
   copy NetEaseMusic /usr/local/bin
   NetEaseMusic
   ```
3. **Pypi**

   ```shell
   pip3 install NetEaseMusicDownloader
   ```

#### Usage:

    Check[Update:2018-09-06](#update2018-09-06)

#### Envrionment:

[Python3.0+](https://www.python.org/downloads/mac-osx/) (with [*requests*](https://github.com/requests/requests) installed.)

[lame](http://lame.sourceforge.net) (use this lib to add Cover for audio.) [Here](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/Install_lame.md) is some instructions.

[Homebrew](https://brew.sh/)

[License](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/LICENSE)

[FFMPEG](http://ffmpeg.org)
