import re

import requests
from bs4 import BeautifulSoup
import time
import json

def perform_search(keyword):
    url = "https://bbs.yamibo.com/search.php?mod=forum"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": ""
    }

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

    response = requests.post(url, headers=headers, data=data, allow_redirects=False)

    if response.status_code == 302:
        search_url = response.headers.get("location")
        if search_url:
            return f"https://bbs.yamibo.com/{search_url}"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("div", id="messagetext", class_="alert_info"):
            print("抱歉，您在 10 秒内只能进行一次搜索")
            time.sleep(10)
            return perform_search(keyword)

    print("Failed to perform search")
    return None


def fetch_and_parse(search_url, page=1):
    url = f"{search_url}&page={page}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return [], 1

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find("div", id="messagetext", class_="alert_info"):
        print("抱歉，您在 10 秒内只能进行一次搜索")
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

    return results, total_pages


def fetch_all_pages(search_url):
    all_results = []
    results, total_pages = fetch_and_parse(search_url, 1)
    all_results.extend(results)

    for page in range(2, total_pages + 1):
        print(f"Fetching page {page}...")
        results, _ = fetch_and_parse(search_url, page)
        all_results.extend(results)

    return all_results


def normalize_titles(results):
    print("\n===== 原始搜索结果 =====")
    display_search_results([(item_id, title) for item_id, title in results])

    base_title = input("\n请输入漫画名称(与过滤搜索无关): ")
    alternative_titles = input("请输入在搜索结果中漫画的所有标题（多个用逗号分隔，此为过滤搜索结果）: ").strip().split(',')
    alternative_titles = [t.strip().lower() for t in alternative_titles if t.strip()]

    print("\n正在处理结果中，请在此期间不要回车...")

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

    print("\n处理完毕")
    return normalized_results

def display_search_results(results):
    for idx, (item_id, original_title) in enumerate(results, 1):
        print(f"{idx}. \t [ID: {item_id}] {original_title}")

def display_results(results):
    for idx, (item_id, base_title, episode_info, full_title) in enumerate(results, 1):
        print(f"{idx}. \t {base_title} \t {episode_info} \t | [ID: {item_id}] {full_title}")


def parse_selection(input_str):
    selected_numbers = set()
    parts = input_str.split(',')
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
        for idx, (item_id, title, episode,_) in enumerate(results, 1) if idx in selected_numbers
    ]
    print(selected_data)
    return selected_data


if __name__ == "__main__":
    keyword = input("请输入搜索关键词: ")
    search_url = perform_search(keyword)

    if search_url:
        results = fetch_all_pages(search_url)
        if results:
            get_results = normalize_titles(results)  # 处理标题
            print("\n===== 处理后的结果 =====")
            display_results(get_results)  # 显示处理后结果

            selected_numbers = input(
                "请选择要提取的条目（用逗号分隔或范围，例如 1-5,8,10-12）："
            )
            selected_numbers = parse_selection(selected_numbers)

            selected_data = get_selected_data(get_results, selected_numbers)
            print("\n===== 最终选择的条目 =====")
            print(json.dumps(selected_data, ensure_ascii=False, indent=4))
    else:
        print("未找到搜索结果。")

