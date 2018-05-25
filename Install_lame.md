# Install Lame Encoder

> **NOTE**: To use *NetEaseMusicDownloader* and add folder or other meta info to music on windows, you should install [Lame](http://lame.sourceforge.net) on windows.

#### Step 1. Download Lame

You can download any from [this page](http://lame.sourceforge.net/download.php). Select the proper file for your system.

#### Step 2. Move downloaded Lame

##### For windows:

>  Then move the download lame encoder(I have download an executable file like below in the screenshot.) into the `C:\Windows\System32` folder. You should have the administrator autherize.

##### For mac / Linux:

> Move the executable binary file into the folder `/usr/local/bin/` or use this command `chmod +x lame && mv lame /usr/local/bin/` in terminal.

#### Step 3. Test lame command.

##### For windows:

>  Open the "CMD", type in `lame`, if print like below, means you have corret installed lame encoder. You can enjoy it

##### For mac / Linux:

> open terminal, type in `lame`. If print like below, means you have installed lame encoder correctly. Enjoy it.
>
> ![](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/screenshots/mac.png)

#### Mac Special 

If you have installed **homebrew**. You can use brew to install lame like this :`brew install lame` in terminal.

> **P.S.** I have not upload the NetEaseMusic.exe file. If you want to use it on windows and you have required environment, you can download the source file(*NetEaseMusic.py*) use *pyinstaller* compiled by yourself. I will upload it ASAP.

# 安装Lame编码器

#### 第一步: 下载Lame

你可以从[这里](http://lame.sourceforge.net/download.php)下载。选择对应系统类型的文件下载。

#### 第二步：移动Lame

##### Windows系统:

>  然后把你下载的Lame编码器（我下载的是一个可执行文件，像下面这样）移动到`C:\Windows\System32`目录。需要有管理员权限。

##### Mac / Linux 系统:

> 把下载的二进制文件移动到`/usr/local/bin`目录或使用命令`chmod +x lame && mv lame /usr/local/bin/`。

#### 第三步：测试Lame命令

##### Windows系统

> 打开"CMD(命令提示符)"窗口，输入`lame`，如果输出像下面这样的话，表示你已经成功安装了Lame编码器。

##### Mac / Linux 系统

> 打开终端，输入`lame`。如果打印的信息像下面这样的话，表示你已经成功安装了Lame编码器。
>
> ![](https://github.com/Kito0615/NetEaseMusicDownloader/blob/master/screenshots/mac.png)

#### Mac安装方法

如果你的电脑中安装了**HomeBrew**的话，你可以在终端中使用`brew install lame`安装。

> **附**: 我现在还没有上传NetEaseMusic.exe文件，如果你想在Windows上使用并且你的电脑中安装有需求的环境的话，你可以自己使用*pyinstaller*自己编译。我会尽快上传的。