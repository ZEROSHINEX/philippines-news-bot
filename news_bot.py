import os
import requests
from telegram import Bot
from bs4 import BeautifulSoup
from googletrans import Translator
from datetime import datetime

# 從環境變數取得 Bot Token 和 Chat ID
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

bot = Bot(token=BOT_TOKEN)
translator = Translator()

# 設定要抓取的新聞網站
def get_news():
    url = 'https://www.philstar.com/headlines'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('.listing li .title a')[:5]

    news_list = []
    for art in articles:
        title = art.text.strip()
        link = art['href']
        if not link.startswith("http"):
            link = "https://www.philstar.com" + link
        news_list.append((title, link))
    return news_list

# 抓取文章內文
def get_article_content(link):
    try:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 根據實際文章的HTML結構選擇適當的標籤
        content = soup.select_one('.article-content-class-name').text.strip()
        return content
    except Exception as e:
        print(f"抓取文章內容失敗：{e}")
        return "（內文抓取失敗，請點擊連結查看完整內容）"

# 翻譯標題與內文
def translate_to_chinese(text):
    try:
        translated = translator.translate(text, dest='zh-tw')
        return translated.text
    except Exception as e:
        print(f"翻譯失敗：{e}")
        return text

# 發送新聞
def send_news():
    message = f"📰 *菲律賓每日新聞快報* ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    news = get_news()

    for title, url in news:
        # 翻譯標題
        zh_title = translate_to_chinese(title)
        # 抓取內文
        content = get_article_content(url)
        # 翻譯內文
        zh_content = translate_to_chinese(content)
        # 合併消息
        message += f"🔹 [{zh_title}]({url})\n{zh_content}\n\n"

    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

send_news()
