import requests
from bs4 import BeautifulSoup

# 抓取單篇文章內文
def get_article_content(link):
    try:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 根據文章的HTML結構選取適當的標籤
        paragraphs = soup.select('.story-block p')
        content = '\n'.join([p.text.strip() for p in paragraphs[:3]])  # 僅取前三段
        return content
    except Exception as e:
        print(f"抓取文章內容失敗：{e}")
        return "（內文抓取失敗，請點擊連結查看完整內容）"

# 測試抓取指定的文章
article_url = 'https://www.philstar.com/headlines/2025/04/17/2436735/a-gift-filipino-nation-marcos-offers-condolences-nora-aunors-family'
content = get_article_content(article_url)
print(content)
