import re

import requests
from bs4 import BeautifulSoup
import time
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from log import log
from utils import request

console = Console()


def perform_search(keyword):
    url = "https://bbs.yamibo.com/search.php?mod=forum"
    data = {
        "srchtxt": keyword,
        "seltableid": "0",
        "srchfilter": "all",
        "srchfrom": "0",
        "orderby": "dateline",
        "ascdesc": "desc",
        "srchfid[]": "30",
        "searchsubmit": "yes"
    }

    response = request.post(url, data=data, allow_redirects=False)

    if response.status_code == 302:
        search_url = response.headers.get("location")
        if search_url:
            log.info(f"成功获取到搜索链接:{search_url}")
            return f"https://bbs.yamibo.com/{search_url}"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("div", id="messagetext", class_="alert_info"):
            log.warning("10秒搜索限制触发，正在等待")
            with console.status("[bold yellow]抱歉，您在 10 秒内只能进行一次搜索，正在等待中...") as status:
                time.sleep(10)
            return perform_search(keyword)

    console.print("[bold red]获取搜索结果失败[/bold red]")
    return None


def fetch_and_parse(search_url, page=1):
    url = f"{search_url}&page={page}"
    response = request.get(url)

    if response.status_code != 200:
        log.error("获取搜索结果失败！" % response.content)
        console.print("[bold red]获取搜索结果失败[/bold red]")
        return [], 1

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find("div", id="messagetext", class_="alert_info"):
        log.warning("10秒搜索限制触发，正在等待")
        with console.status("[bold yellow]抱歉，您在 10 秒内只能进行一次搜索，正在等待中...") as status:
            time.sleep(10)
        return fetch_and_parse(search_url, page)

    total_pages = 1
    page_info = soup.find("span", title=lambda x: x and "共" in x and "页" in x)
    if page_info:
        total_pages = int(page_info.text.split("/")[-1].strip().replace("页", ""))

    items = soup.find_all("li", class_="pbw")

    results = []
    for item in items:
        item_id = item.get("id", "N/A")
        h3_tag = item.find("h3", class_="xs3")

        if h3_tag and h3_tag.a:
            title = h3_tag.a.get_text(strip=True)
            results.append((item_id, title))
    log.info(f"当前页面搜索结果获取完毕：{results}")
    return results, total_pages


def fetch_all_pages(search_url):
    all_results = []
    results, total_pages = fetch_and_parse(search_url, 1)
    all_results.extend(results)

    for page in range(2, total_pages + 1):
        log.info(f"正在获取第 {page} 页数据")
        console.print(f"[blue]正在获取第 {page} 页数据...")
        results, _ = fetch_and_parse(search_url, page)
        all_results.extend(results)
    log.info(f"所有搜索结果获取完毕：{results}")
    return all_results


def normalize_titles(results):
    console.rule(f"[bold blue]搜索结果[/bold blue]")
    display_search_results([(item_id, title) for item_id, title in results])

    base_title = Prompt.ask("\n请输入漫画名称(与过滤搜索无关)")
    alternative_titles = Prompt.ask(
        "请输入在搜索结果中漫画的所有标题（多个用逗号分隔，此为过滤搜索结果）").strip().split(',')
    alternative_titles = [t.strip().lower() for t in alternative_titles if t.strip()]

    with console.status("[bold green]正在处理搜索结果中...") as status:
        log.info("开始处理搜索结果")
        # 处理可能的标题变体
        title_variants = {base_title.lower()} | {t.strip().lower() for t in alternative_titles if t.strip()}

        normalized_results = []
        for item_id, full_title in results:
            matched_variant = None
            episode_info = ""

            for variant in title_variants:
                lower_title = full_title.lower()
                pattern = rf"{re.escape(variant)}\s*(.*)"
                match = re.search(pattern, lower_title)
                if match:  # 确保是以该标题开头的
                    remaining_part = match.group(1)  # 提取标题后内容（去掉开头空格）
                    matched_variant = variant
                    episode_info = remaining_part
                    break

            if matched_variant:
                normalized_results.append((item_id, base_title, episode_info, full_title))
    log.info(f"处理搜索结果完毕：{normalized_results}")
    return normalized_results


def display_search_results(results):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("序号")
    table.add_column("帖子ID")
    table.add_column("标题")
    for idx, (item_id, original_title) in enumerate(results, 1):
        table.add_row(
            str(idx), item_id, original_title
        )
    console.print(table)


def display_results(results):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("序号")
    table.add_column("漫画名称")
    table.add_column("章节标题")
    table.add_column("帖子ID")
    table.add_column("帖子标题")
    for idx, (item_id, base_title, episode_info, full_title) in enumerate(results, 1):
        table.add_row(
            str(idx), base_title, episode_info, item_id, full_title
        )
    console.print(table)


def parse_selection(input_str):
    selected_numbers = set()
    parts = input_str.split(',')
    log.info(f"用户选择序号：{parts}")
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            selected_numbers.update(range(start, end + 1))
        else:
            selected_numbers.add(int(part))
    return selected_numbers


def get_selected_data(results, selected_numbers):
    selected_data = [
        {"id": item_id, "title": title, "episode": episode}
        for idx, (item_id, title, episode, _) in enumerate(results, 1) if idx in selected_numbers
    ]
    return selected_data

def search():
    keyword = Prompt.ask("请输入搜索关键词")
    search_url = perform_search(keyword)

    if search_url:
        with console.status("[bold green]正在搜索中...") as status:
            results = fetch_all_pages(search_url)
        if results:
            get_results = normalize_titles(results)  # 处理标题
            console.rule(f"[bold blue]漫画列表[/bold blue]")
            display_results(get_results)  # 显示处理后结果

            selected_numbers = Prompt.ask(
                "请选择要提取的条目（输入A全选，用逗号分隔或范围，例如 1-5,8,10-12）"
            )
            selected_numbers = parse_selection(selected_numbers)

            selected_data = get_selected_data(get_results, selected_numbers)
            print("\n===== 最终选择的条目 =====")
            console.print(json.dumps(selected_data, ensure_ascii=False, indent=4))
    else:
        console.print("[red]未找到搜索结果。[/red]")


if __name__ == "__main__":
    search()