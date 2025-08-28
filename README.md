# 🔍 Google SERP & SEO Sıralama API

Bu API, **Google arama sonuçlarını (SERP)** çekmek için geliştirilmiş bir **Flask tabanlı web servisi**dir.  
Verilen parametreler ile Google üzerinde arama yapar ve ilk **10 sonucu JSON formatında döndürür**.  

> 📌 API, SEO uzmanları, yazılım geliştiriciler ve dijital pazarlamacılar için uygundur.  
> Kendi arayüzünüzü geliştirip API’yi kolayca entegre edebilirsiniz.

---

## 🚀 Canlı API

**Base URL:**  
https://flask-search-api-3fox.onrender.com

makefile
Kodu kopyala

**Endpoint:**  
/search

markdown
Kodu kopyala

**Yöntem:** `GET`  
**Yanıt Tipi:** `application/json`  
**CORS:** ✅ Aktif (Frontend’den doğrudan kullanılabilir)

---

## 📌 Parametreler (Tümü Zorunlu)

| Parametre      | Açıklama                                | Örnek Değer    |
|---------------|---------------------------------------|---------------|
| `query`       | Aranacak anahtar kelime               | openai        |
| `dil`         | Google arama dili                     | tr            |
| `bolge`       | Google arama bölgesi                  | tr            |
| `device`      | Cihaz türü: `desktop` veya `mobile`   | desktop       |
| `site_filter` | Takip etmek istediğiniz alan adı      | openai.com    |

---

## 🎯 API’nin Özellikleri

- 🔎 Google üzerinde belirtilen anahtar kelime için arama yapar  
- 📌 İlk **40 sonucu** JSON formatında döndürür  
- 🏷️ Her sonucun **sıra numarası**, **URL**, **domain**, **başlık** ve **meta açıklamasını** verir  
- ✅ Belirtilen `site_filter` URL’si sonucu içeriyorsa `hedef_site_mi: true` döner  
- ❌ **Hedef site sırasını veya özet rapor vermez**  
- 📱 Desktop ve mobil cihazlar için farklı User-Agent desteği vardır  

---

## ⚡ Örnek Sorgu

**Örnek URL:**  
https://flask-search-api-3fox.onrender.com/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com

pgsql
Kodu kopyala

---

## ✅ Örnek JSON Yanıtı

```json
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
    "url": "https://en.wikipedia.org/wiki/OpenAI",
    "domain": "wikipedia.org",
    "baslik": "OpenAI - Wikipedia",
    "aciklama": "OpenAI, yapay zeka üzerine çalışan bir şirkettir.",
    "hedef_site_mi": false
  },
  {
    "sira": 3,
    "url": "https://medium.com/@openai",
    "domain": "medium.com",
    "baslik": "OpenAI Blog",
    "aciklama": "OpenAI tarafından yayınlanan makaleler ve duyurular.",
    "hedef_site_mi": false
  }
]
```
Not: Bu API, hedef sitenin kaçıncı sırada olduğunu hesaplamaz.
Sadece sonuçlar arasında olup olmadığını kontrol etmeniz gerekir.

🧩 API Entegrasyon Örnekleri
JavaScript ile
javascript
Kodu kopyala
const params = {
  query: "openai",
  dil: "tr",
  bolge: "tr",
  device: "desktop",
  site_filter: "openai.com"
};

const url = new URL("https://flask-search-api-3fox.onrender.com/search");
Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

fetch(url)
  .then(res => res.json())
  .then(data => {
    console.log("Sonuçlar:", data);
    data.forEach(item => {
      console.log(`${item.sira}. ${item.baslik} (${item.url}) — Hedef site mi? ${item.hedef_site_mi}`);
    });
  })
  .catch(err => console.error("Hata:", err));

Python ile

import requests

url = "https://flask-search-api-3fox.onrender.com/search"
params = {
    "query": "openai",
    "dil": "tr",
    "bolge": "tr",
    "device": "desktop",
    "site_filter": "openai.com"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    for r in data:
        print(f"{r['sira']}. {r['baslik']} -> {r['url']} | Hedef site mi? {r['hedef_site_mi']}")
else:
    print("Hata:", response.status_code, response.text)


cURL ile

curl "https://flask-search-api-3fox.onrender.com/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com"


📊 Kullanım Senaryoları
🔹 Google Arama Sonuçları Çekme → İlk 40 sonucu JSON formatında al

🔹 Site Varlık Kontrolü → Belirli bir domain sonuçlar arasında var mı?

🔹 Mobil & Desktop Karşılaştırması → Cihaz bazlı sonuç farklarını bulma

🔹 SEO Analizi → Rakip sitelerin başlık ve meta açıklamalarını inceleme

🔹 Otomasyon Sistemleri → Kendi SEO paneline entegre etme

🛠 Lokal Kurulum

git clone https://github.com/kullanici/flask-search-api.git
cd flask-search-api
pip install -r requirements.txt
python app.py

API şu adreste çalışır:

http://127.0.0.1:5000/search?query=openai&dil=tr&bolge=tr&device=desktop&site_filter=openai.com
