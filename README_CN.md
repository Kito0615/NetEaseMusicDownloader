# NetEaseMusicDownloader

[README.md](https://github.com/Kito0615/NetEaseMusicDownloader/raw/master/README.md) 

> **注意:** 这个脚本使用了[AD's API](https://api.imjad.cn/) 提供的接口，在此表示感谢. 这个脚本仅供个人学习交流使用，不能用于任何商业用途，所有法律问题均与作者无关。

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

Python3.0+

Homebrew

[License](http://github.com/Kito0615/NetEaseMusicDownloader/row/master/MIT.md)

