# NetEaseMusicDownloader

[README.md](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/README.md) 

![](https://img.shields.io/badge/Platform-Python3-009eff.svg) ![](https://img.shields.io/badge/Windows-Unsupported-ff005f.svg)  ![](https://img.shields.io/badge/MacOS-Supported-00efff.svg) ![](https://img.shields.io/badge/Linux-Supported-00efff.svg)

> **注意:** 这个脚本使用了[AD's API](https://api.imjad.cn/) 提供的接口，在此表示感谢. 这个脚本仅供个人学习交流使用，不能用于任何商业用途，所有法律问题均与作者无关。
>
> **注意**: 新添加的[QQ音乐](http://y.qq.com)的接口来自其网站，**版权归[QQ音乐](http://y.qq.com)所有**。仅供**学习交流**使用

#### 更新: 2018-05-22

1. 现在可以使用工具下载歌曲/歌单/专辑了。使用*AD's API*。

#### 更新：2018-05-17

1. 当[网易云音乐](http://music.163.com) 音乐资源不可用时，增加新的搜索源[QQ音乐](http://y.qq.com)。
2. 增加新的依赖库[FFMPEG](http://ffmpeg.org)，用来转换从QQ音乐下载的*.m4a*文件为*.mp3*。

#### 下载:

1. **下载完整工程**

   ```shell
   git clone https://github.com/Kito0615/NetEaseMusic.git	
   ```

   在终端直接运行脚本源码文件(NetEaseMusic.py)。需要python3环境。

   ```shell
   python3 NetEaseMusic.py
   ```

   或者:

   ```shell
   chmod +x NetEaseMusic.py
   ./NetEaseMusic.py
   ```

2. **下载发布文件**

   点击 [这里](https://github.com/Kito0615/NetEaseMusicDownloader/releases), 下载你需要的版本. 再在终端执行:

   ```shell
   ./NetEaseMusic
   ```

   或者拷贝二进制文件到 `/usr/local/bin`, 然后你就可以在任何目录执行:

   ```shell
   NetEaseMusic
   ```

   ​

#### 用法:

当你拷贝二进制文件到 `/usr/local/bin` 目录后，有几种执行方式:

1. **在终端直接输入:**

   ```shell
   NetEaseMusic	
   ```

2. **在程序后面输入链接地址:**

   ```shell
   NetEaseMusic [url]	
   ```

   这样表示直接下载链接[url]对应页面的歌曲

3. **在程序后面输入链接地址和目标文件夹:**

   ```shell
   NetEaseMusic [url] [folder]
   ```

   这样表示从链接[url]对应页面下载歌曲到指定目录[folder]

#### 环境:

[Python3.0+](https://www.python.org/downloads/mac-osx/) (需要安装[*requests*](https://github.com/requests/requests)库)

[lame](http://lame.sourceforge.net) (用于给音乐添加封面)

[Homebrew](https://brew.sh/) 

[License](http://github.com/Kito0615/NetEaseMusicDownloader/blob/master/MIT.md)

[FFMPEG](http://ffmpeg.org)

