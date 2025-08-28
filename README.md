# 🔍 Flask Google Search API

Bu proje, **Flask** tabanlı bir API olup, **Google üzerinden arama** yaparak sonuçları **JSON** formatında döndürür. Başlık/açıklama çekilmez; sadece `url`, `domain` ve `hedef_site_mi` alanları döner. Uygulama Railway üzerinde barındırılmaktadır.

- Canlı URL: **https://web-production-27b2c.up.railway.app**
- Geliştirici: **@alperkoyun**

---

## 📌 Özellikler
- Google araması (googlesearch-python)
- JSON çıktı: `sira`, `url`, `domain`, `hedef_site_mi`
- **20 sonuç** döndürür
- `device` desteği: `desktop`, `mobile`, `tablet`

---

## 🛠️ Kurulum (Yerel)

```bash
git clone https://github.com/alperkoyun/flask-google-search-api.git
cd flask-google-search-api
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```



⚡ Örnek İstekler
```bash
Desktop:

curl "https://web-production-27b2c.up.railway.app/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com"


Mobile:

curl "https://web-production-27b2c.up.railway.app/search?query=openai&dil=tr&bolge=tr&device=mobile&site_filter=openai.com"


Tablet:

curl "https://web-production-27b2c.up.railway.app/search?query=openai&dil=tr&bolge=tr&device=tablet&site_filter=openai.com"

🧪 Örnek Yanıt
[
  { "sira": 1, "url": "https://openai.com/", "domain": "openai.com", "hedef_site_mi": true },
  { "sira": 2, "url": "https://platform.openai.com/", "domain": "platform.openai.com", "hedef_site_mi": true }
  // ... toplam 20 sonuç
]

```