from rich.console import Console

from downloader import downloader
from search import search
from utils import config

console = Console()


def main():
    console.print(
        "[bold green]感谢使用[/bold green][bold yellow]yamibo-downloader[/bold yellow][bold green]！如果可以能去仓库点个:glowing_star:吗qwq[/bold green]")
    if not config.COOKIE or not config.DOWNLOAD_PATH:
        console.print("[bold red]请检查.env文件，及根据github中的README进行配置[/bold red]")
        exit(1)
    # Todo 支持直接输入帖子ID进行下载
    list = search()
    if not list:
        exit(1)
    downloader(list)


if __name__ == '__main__':
    main()
