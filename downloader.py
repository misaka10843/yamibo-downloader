import os
import re
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo
from cbz.player import PARENT
from rich.console import Console
from rich.progress import track

from utils import request, config
from utils.log import log

console = Console()


def download(url, filename):
    log.info(f"开始下载图片，URL：{url}，路径：{filename}")
    response = request.get(url)
    if not response:
        log.error(f"图片下载失败，URL：{url}")
        console.print(f"[bold red]无法下载{filename}，请稍后手动下载对应章节(章节话数为每话下载输出的帖子ID)[/]")
        return
    with open(filename, "wb") as f:
        f.write(response.content)


def after_download(title, episode):
    if config.PACKAGED_CBZ:
        console.print("[bold green]开始打包cbz[/bold green]")
        path = f"{config.DOWNLOAD_PATH}/{title}/{episode}/"
        paths = list(Path(path).iterdir())
        pages = [
            PageInfo.load(
                path=path,
                type=PageType.FRONT_COVER if i == 0 else PageType.STORY
            )
            for i, path in enumerate(paths)
        ]

        comic = ComicInfo.from_pages(
            pages=pages,
            title=title,
            series=title,
            language_iso='zh',
            number=episode,
            format=Format.WEB_COMIC,
            black_white=YesNo.NO,
            manga=Manga.YES,
            age_rating=AgeRating.PENDING
        )
        cbz_content = comic.pack()
        if config.CBZ_PATH:
            path = f"{config.CBZ_PATH}/{title}/"
        else:
            path = f"{config.DOWNLOAD_PATH}/{title}/"
        if not os.path.exists(path):
            os.makedirs(path)
        cbz_path = PARENT / f'{path}/{episode}.cbz'
        cbz_path.write_bytes(cbz_content)

        if not config.KEEP_IMAGE:
            console.print("[bold green]开始删除原文件[/bold green]")
            os.remove(f"{config.DOWNLOAD_PATH}/{title}/{episode}/")


def downloader(list):
    for item in list:
        title = item["title"]
        episode = item["episode"]
        id = item["id"]
        console.print(f"[bold green]正在获取[{title}]{episode}(帖子ID:{id})的信息[/]")
        url = f"https://bbs.yamibo.com/api/mobile/index.php?module=viewthread&tid={id}"
        response = request.get(url)

        if not response:
            log.error(f"获取帖子信息失败，ID：{id}，返回：{response.content}")
            console.print(f"[bold red]无法获取此信息，请稍后手动下载对应章节(章节话数为每话下载输出的帖子ID)[/]")
            break
        log.info(f"获取帖子信息成功，ID：{id}，返回：{response.content}")
        data = response.json()['Variables']['postlist'][0]

        for i in track(range(len(data["imagelist"])),
                       description=f"[bold yellow]正在下载:[{title}]{episode}(帖子ID:{id})"):
            # 组成下载路径
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            episode = re.sub(rstr, "_", episode)  # 替换为下划线
            save_path = f"{config.DOWNLOAD_PATH}/{title}/{episode}"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            # 解析API返回数据
            for index, image_key in enumerate(data["imagelist"], start=1):
                attachment_url = data["attachments"].get(image_key, {}).get("attachment")
                filename = f"{save_path}/{str(index).zfill(4)}.jpg"
                url = f"https://bbs.yamibo.com/data/attachment/forum/{attachment_url}"
                download(url, filename)
        with console.status("[bold green]正在运行下载后程序中...") as status:
            after_download(title, episode)
