from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS modülünü içeri aktar


from googlesearch import search
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

app = Flask(__name__)
CORS(app)  # CORS desteğini etkinleştiriyoruz

# Mobil ve Masaüstü User-Agent'leri
USER_AGENT_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148"
USER_AGENT_DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Web sayfası detaylarını alma
def get_page_details(url, user_agent):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Başlık
        title = soup.title.string.strip() if soup.title else "Başlık bulunamadı"

        # Meta description
        desc = soup.find("meta", attrs={"name": "description"})
        description = desc["content"].strip() if desc and "content" in desc.attrs else "Açıklama bulunamadı"

        return title, description
    except Exception as e:
        return "Başlık alınamadı", "Açıklama alınamadı"

# Google aramasını JSON formatında döndüren fonksiyon
def google_search_to_json(query, dil=None, bolge=None, device=None, site_filter=None):
    results = []

    # User-Agent'ı belirle (Mobil ya da Masaüstü)
    if device == "mobile":
        user_agent = USER_AGENT_MOBILE
    else:
        user_agent = USER_AGENT_DESKTOP

    # Google araması parametrelerini ayarla
    search_params = {
        'num_results': 40,
        'lang': dil,
        'region': bolge,
        'unique': True
    }

    for i, url in enumerate(search(query, **search_params), start=1):
        title, description = get_page_details(url, user_agent)
        domain = urlparse(url).netloc

        result = {
            "sira": i,
            "url": url,
            "domain": domain,
            "baslik": title,
            "aciklama": description,
            "hedef_site_mi": (site_filter in url) if site_filter else False
        }

        results.append(result)

    return results

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query')
    dil = request.args.get('dil', default="tr")
    bolge = request.args.get('bolge', default="tr")
    device = request.args.get('device', default=None)
    site_filter = request.args.get('site_filter', default=None)

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Arama ve sonuçları JSON formatında döndür
    results = google_search_to_json(query, dil=dil, bolge=bolge, device=device, site_filter=site_filter)

    # Yanıtı kontrol et
    if not results:
        print("Arama sonucu bulunamadı.")

    return jsonify(results)

# API'yi çalıştır
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
