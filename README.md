# 🔍 Flask Google Search API  
Bu proje, **Flask** tabanlı bir API olup, **Google üzerinden arama** yaparak sonuçları **JSON** formatında döndürür.  
**meta=1** (yavaş mod) ile başlık & açıklama bilgileri çekilir, **meta=0** (hızlı mod) ile sadece URL ve domain döner.  
Render **Free planı** için optimize edilmiştir. 🚀  

---

## 📌 Özellikler  
- 🔹 **Google Search API** (googlesearch-python)  
- 🔹 **meta=1** → Başlık & açıklamalar paralel olarak çekilir  
- 🔹 **meta=0** → Hızlı mod, sadece URL & domain döner  
- 🔹 **Desktop / Mobile** cihaz desteği  
- 🔹 **CORS açık** → Tüm frontend uygulamalarıyla uyumlu  
- 🔹 Render **free planı** için optimizasyonlar:  
  - Varsayılan hızlı mod (`meta=0`)  
  - Maksimum **15 sonuç** döndürür  
  - **3 saniye timeout** → Render 90s limitine uygun  
  - **2 worker + 4 thread** → Daha az RAM ve CPU kullanır  

---

## 🛠️ Kurulum  

### 1️⃣ Depoyu Klonla  
```bash
git clone https://github.com/alperkoyun/flask-google-search-api.git
cd flask-google-search-api
```

2️⃣ Sanal Ortam Oluştur
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3️⃣ Bağımlılıkları Kur
```bash
pip install -r requirements.txt
```

4️⃣ Lokal Sunucuyu Başlat
```bash
python app.py

Sunucu çalıştığında:

http://127.0.0.1:5000
```

⚡ Örnek Sorgular
```bash
1️⃣ Hızlı Mod (meta=0) — Varsayılan
curl "http://127.0.0.1:5000/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com&meta=0"

2️⃣ Yavaş Mod (meta=1) — Başlık & Açıklama ile
curl "http://127.0.0.1:5000/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com&meta=1"

🧪 Örnek Yanıt
[
  {
    "sira": 1,
    "url": "https://openai.com/",
    "domain": "openai.com",
    "baslik": "OpenAI",
    "aciklama": "OpenAI, yapay zeka araştırmaları yapan bir şirkettir.",
    "hedef_site_mi": true
  },
  {
    "sira": 2,
    "url": "https://platform.openai.com/",
    "domain": "platform.openai.com",
    "baslik": "OpenAI API",
    "aciklama": "OpenAI API, GPT modellerine kolay erişim sağlar.",
    "hedef_site_mi": true
  }
]
```