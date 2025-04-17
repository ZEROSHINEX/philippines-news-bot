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

# 翻譯標題
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
        zh_title = translate_to_chinese(title)
        message += f"🔹 [{zh_title}]({url})\n"

    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

send_news()
