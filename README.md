# NetEaseMusicDownloader

[中文说明](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/README_CN.md) 

> **NOTE:** In this script, I used some api via [AD's API](https://api.imjad.cn/). Thanks. This 
> script is for personal use only. It cannot be used for any commercial 
> activities. All legal issues are not related to the author.

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

   ​

#### Usage:

There are a few ways to execute the binary when you copy to `/usr/local/bin`:

1. **Directly run command in terminal:**

   ```shell
   NetEaseMusic	
   ```

2. **Add the url follow the command:**

   ```shell
   NetEaseMusic [url]	
   ```

   This means download music from the following [url] page.

3. **Add the folder and the url follow the command :**

   ```shell
   NetEaseMusic [url] [folder]
   ```

   This means download music from the following [url] page to the destination [folder].

#### Envrionment:

Python3.0+(with *requests* installed.)

libmp3lame(use this lib to add Cover for audio.)

Homebrew

[License](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/MIT.md)