# yamibo-downloader

百合会论坛漫画下载器

可以批量下载百合会论坛中帖子中的漫画，非常适合将本程序挂在一边自动下载大范围的漫画

并不适合下载小范围话数的情况（因为下载一话为了防止出错可能需要3-5分钟左右）

## 前排提醒

因为论坛的原因，无法用一种对用户很友好的方式类似漫画网站的章节列表形式进行下载

也就是说，在使用类似范围选择下载话方式时，可能有概率下载出错/下载掉页等任何问题

除非是仅下载单独一话/提供所有话的URL才可能可以下载完整（毕竟没有任何API可以操作，完全读取html）

此下载器处于在建状态，请注意任何不稳定的问题！

与本人制作的其他下载器不同，此下载器仅仅只为了能够一时脑热自己手动进行下载，不支持订阅下载等功能(懒得花时间写x)

因为百合会服务器的图片有速率限制，现在暂且摸清5-10秒一次可以防止403

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
![image](https://github.com/user-attachments/assets/f684d152-bccf-4f4a-9927-7d278a88475c)

