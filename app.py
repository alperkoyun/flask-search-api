from flask import Flask, request, jsonify
from flask_cors import CORS
from googlesearch import search
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)  # CORS açık

# User-Agent'ler
USER_AGENT_DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
USER_AGENT_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148"
USER_AGENT_TABLET = "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"

# Google araması yapan fonksiyon
def google_search_to_json(query, dil="tr", bolge="tr", device="desktop", site_filter=None, num_results=20):
    results = []

    # User-Agent seçimi
    if device == "mobile":
        user_agent = USER_AGENT_MOBILE
    elif device == "tablet":
        user_agent = USER_AGENT_TABLET
    else:
        user_agent = USER_AGENT_DESKTOP

    search_params = {
        "num_results": num_results,
        "lang": dil,
        "region": bolge,
        "unique": True
    }

    urls = list(search(query, **search_params))

    for i, url in enumerate(urls, start=1):
        results.append({
            "sira": i,
            "url": url,
            "domain": urlparse(url).netloc,
            "hedef_site_mi": (site_filter in url) if site_filter else False
        })

    return results

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query')
    dil = request.args.get('dil', default="tr")
    bolge = request.args.get('bolge', default="tr")
    device = request.args.get('device', default="desktop")
    site_filter = request.args.get('site_filter')

    if not query:
        return jsonify({"error": "query parametresi zorunludur"}), 400

    try:
        results = google_search_to_json(
            query=query,
            dil=dil,
            bolge=bolge,
            device=device,
            site_filter=site_filter,
            num_results=20
        )
    except Exception as e:
        return jsonify({"error": "Arama sırasında bir hata oluştu", "detail": str(e)}), 502

    if not results:
        return jsonify({"message": "Sonuç bulunamadı"}), 404

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
