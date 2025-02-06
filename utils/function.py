import time

from utils import config


def api_restriction():
    config.API_COUNTER += 1
    if config.API_COUNTER >= 30:
        config.API_COUNTER = 0
        print("[bold yellow]您已经触发到了API请求阈值，我们将等60秒后再进行[/]")
        time.sleep(60)
