import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv(verbose=True)
# 尝试从环境变量中获取配置值
COOKIE = os.getenv("COOKIE")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH")
PACKAGED_CBZ = os.getenv("PACKAGED_CBZ") or False
