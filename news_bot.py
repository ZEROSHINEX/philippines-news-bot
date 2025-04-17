import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Bot
from googletrans import Translator
import schedule
import time

# 從環境變數取得 Telegram Bot 的資訊
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = Bot(token=BOT_TOKEN)

# 初始化翻譯器
translator = Translator()

# ========== 爬蟲：Philippine Star ==========
def get_philstar_news():
    url = 'https://www.philstar.com/headlines'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('.listing li .title a')[:5]
    news_list = []
    for art in articles:
        title = art.text.strip()
        link = art.get('href')
        if not link.startswith("http"):
            link = "https://www.philstar.com" + link
        news_list.append((title, link))
    return news_list

# ========== 爬蟲：Inquirer.net ==========
def get_inquirer_news():
    url = 'https://newsinfo.inquirer.net/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('article .td-module-title a')[:5]
    news_list = []
    for art in articles:
        title = art.text.strip()
        link = art.get('href')
        news_list.append((title, link))
    return news_list

# ========== 翻譯英文標題 ==========
def translate_to_chinese(text):
    try:
        translated = translator.translate(text, dest='zh-tw')
        return translated.text
    except Exception as e:
        print(f"翻譯失敗：{e}")
        return text

# ========== 發送訊息 ==========
def send_news():
    message = f"📰 *菲律賓每日新聞快報* ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    
    philstar_news = get_philstar_news()
    inquirer_news = get_inquirer_news()
    
    message += "*📌 Philippine Star*\n"
    for title, url in philstar_news:
        zh_title = translate_to_chinese(title)
        message += f"🔹 [{zh_title}]({url})\n"
    
    message += "\n*📌 Inquirer.net*\n"
    for title, url in inquirer_news:
        zh_title = translate_to_chinese(title)
        message += f"🔹 [{zh_title}]({url})\n"
    
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

# ========== 排程每日一次 ==========
schedule.every().day.at("08:00").do(send_news)

print("✅ 新聞爬蟲已啟動，每天 08:00 自動推播中...")
while True:
    schedule.run_pending()
    time.sleep(60)
