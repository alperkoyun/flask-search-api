from flask import Flask, request, jsonify
from flask_cors import CORS
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)  # CORS desteği

# User-Agent'ler
USER_AGENT_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148"
USER_AGENT_DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Web sayfası başlık ve meta açıklama çekme
def get_page_details(url, user_agent):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "Başlık bulunamadı"
        desc = soup.find("meta", attrs={"name": "description"})
        description = desc["content"].strip() if desc and "content" in desc.attrs else "Açıklama bulunamadı"

        return title, description
    except Exception:
        return "Başlık alınamadı", "Açıklama alınamadı"

# Google araması yapan fonksiyon
def google_search_to_json(query, dil=None, bolge=None, device=None, site_filter=None, meta=True):
    results = []
    user_agent = USER_AGENT_MOBILE if device == "mobile" else USER_AGENT_DESKTOP

    search_params = {
        'num_results': 10,
        'lang': dil,
        'region': bolge,
        'unique': True
    }

    urls = list(search(query, **search_params))

    # Hızlı mod (meta=0) → başlık & açıklama çekilmez
    if not meta:
        for i, url in enumerate(urls, start=1):
            domain = urlparse(url).netloc
            results.append({
                "sira": i,
                "url": url,
                "domain": domain,
                "baslik": "Başlık alınmadı (meta=0)",
                "aciklama": "Açıklama alınmadı (meta=0)",
                "hedef_site_mi": (site_filter in url) if site_filter else False
            })
        return results

    # Yavaş mod (meta=1) → başlık & açıklama paralel çekilir
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_page_details, url, user_agent): url for url in urls}
        i = 1
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            domain = urlparse(url).netloc
            try:
                title, description = future.result()
            except Exception:
                title, description = "Başlık alınamadı", "Açıklama alınamadı"

            results.append({
                "sira": i,
                "url": url,
                "domain": domain,
                "baslik": title,
                "aciklama": description,
                "hedef_site_mi": (site_filter in url) if site_filter else False
            })
            i += 1

    results.sort(key=lambda x: x["sira"])
    return results

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query')
    dil = request.args.get('dil', default="tr")
    bolge = request.args.get('bolge', default="tr")
    device = request.args.get('device', default="desktop")
    site_filter = request.args.get('site_filter', default=None)
    meta_flag = request.args.get('meta', default="0")
    meta = meta_flag != "0"

    if not query:
        return jsonify({"error": "query parametresi zorunludur"}), 400

    results = google_search_to_json(query, dil=dil, bolge=bolge, device=device, site_filter=site_filter, meta=meta)

    if not results:
        return jsonify({"message": "Sonuç bulunamadı"}), 404

    return jsonify(results)

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000)


