> [!WARNING]
> **因为尽可能缓解copymanga服务器压力，此程序限制了每分钟只能访问15次API，还请理解！**
>
> **我并不希望此工具影响到百合会的运行，所以此下载器比其他本人编写的下载器更加的难用(绝对不是自己懒)，**
>
> **请不要自行改写本下载器/使用本下载器原理制作其他类型下载器而不添加API请求限制！**
>
> **对于使用绝大部份的第三方小网站的下载器都是同理，服务器流量真的很贵，如果为了用户体验可能还会套上cdn会更贵，如果爬虫泛滥可能还会用Cloudflare等手段阻止爬虫。
**

# yamibo-downloader

百合会论坛漫画下载器(WIP)

## 前排提醒

因为论坛的原因，无法用一种对用户很友好的方式类似漫画网站的章节列表形式进行下载

也就是说，在使用类似范围选择下载话方式时，可能有概率下载出错/下载掉页等任何问题

除非是仅下载单独一话/提供所有话的URL才可能可以下载完整（毕竟没有任何API可以操作，完全读取html）

此下载器处于在建状态，请注意任何不稳定的问题！

与本人制作的其他下载器不同，此下载器仅仅只为了能够一时脑热自己手动进行下载，不支持订阅下载等功能(懒得花时间写x)

以本人的习惯，为了尽可能减轻百合会服务器负担，本下载器已设置15次/分钟的请求，请不要自行解开

请任何人需要注意一点！不要修改本下载器的API速率限制，也不要用本下载器使用的API/数据获取的方法自行制作下载器但不添加API速率限制

如果本人发现，将不会维护所有下载器仓库以及其他网站的下载器将不会进行开源，还请理解！（真的，真的希望大家能够友好使用而不是图一时之快！！！！）

## 为什么制作这个下载器？

其实说句实话在当前大多数漫画网站都获取不了这么清晰的原图，并且因为论坛的特性在手机端上无法使用其他任何一款阅读器进行阅读

而在PC端上也存在着类似问题

为了缓解百合会服务器压力（我一话多看几遍（去缓存）的话还不如下载一遍本地来看（bushi）），以及方便下载漫画而制作本下载器

## 如何使用

可以前往[releases](https://github.com/misaka10843/yamibo-downloader/releases)下载各个平台的打包程序

然后将[.env.example](https://github.com/misaka10843/yamibo-downloader/blob/main/.env.example)重命名为`.env`并放在程序的同级目录下

修改`.env`文件，其中对应关系如下：

```dotenv
COOKIE="" #百合会的cookie字段
DOWNLOAD_PATH="" #下载的保存路径
PACKAGED_CBZ=False/True #是否打包成CBZ，如果打包
KEEP_IMAGE=False/True #在打包CBZ为True是否保存原文件？
CBZ_PATH="" #CBZ保存路径
```

打开cmd并cd进程序的同级目录下运行`./yamibo-downloader`即可

## 一些截图

搜索界面：

![image](https://github.com/user-attachments/assets/91e0d7db-9d6d-4b88-b57c-5b0b43aceec1)

漫画选择界面：

![image](https://github.com/user-attachments/assets/3d79a517-b0c8-44a0-a08d-f85068230b23)

下载界面：

![image](https://github.com/user-attachments/assets/5acd9a61-3670-4b67-9983-31264de9aaa7)
