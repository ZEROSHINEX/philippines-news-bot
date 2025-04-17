import requests
from bs4 import BeautifulSoup

# 設定目標網站的URL
def get_asgam_news():
    url = 'https://zh.asgam.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # 選擇首頁上的新聞標題和連結
    articles = soup.select('.item-title > a')[:5]  # 假設 class 為 item-title 並包含 <a>
    
    news_list = []
    for art in articles:
        title = art.text.strip()
        link = art['href']
        if not link.startswith("http"):
            link = "https://zh.asgam.com" + link
        news_list.append((title, link))
    return news_list

# 抓取文章內文
def get_article_content(link):
    try:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 根據實際文章的HTML結構選取適當的內文標籤
        paragraphs = soup.select('.post-content p')  # 假設文章內文在 post-content 的 <p> 中
        content = '\n'.join([p.text.strip() for p in paragraphs[:3]])  # 僅取前三段
        return content
    except Exception as e:
        print(f"抓取文章內容失敗：{e}")
        return "（內文抓取失敗，請點擊連結查看完整內容）"

# 測試抓取新聞列表
news = get_asgam_news()
print("=== 新聞標題和連結 ===")
for title, link in news:
    print(title, link)

# 測試抓取某篇文章的內文
if news:
    test_link = news[0][1]  # 測試第一篇文章的連結
    content = get_article_content(test_link)
    print("\n=== 測試文章內文 ===")
    print(content)
