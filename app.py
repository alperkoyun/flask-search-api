from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse
import requests
import os

app = Flask(__name__)
CORS(app)

# Public SearXNG instance
SEARXNG_URL = os.environ.get("SEARXNG_URL", "https://searx.tiekoetter.com")

def searxng_search_to_json(query, dil="tr", site_filter=None, num_results=20):
    params = {
        "q": query,
        "format": "json",
        "language": dil,
        "safesearch": 0,
        "category_general": 1
    }

    r = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    results = []
    for i, item in enumerate(data.get("results", [])[:num_results], start=1):
        url = item.get("url")
        domain = urlparse(url).netloc if url else ""

        results.append({
            "sira": i,
            "url": url,
            "domain": domain,
            "baslik": item.get("title"),
            "aciklama": item.get("content"),
            "hedef_site_mi": (site_filter in url) if (site_filter and url) else False
        })

    return results


@app.route("/search", methods=["GET"])
def search_api():
    query = request.args.get("query")
    dil = request.args.get("dil", default="tr")
    site_filter = request.args.get("site_filter")

    if not query:
        return jsonify({"error": "query parametresi zorunludur"}), 400

    try:
        results = searxng_search_to_json(
            query=query,
            dil=dil,
            site_filter=site_filter,
            num_results=20
        )
    except Exception as e:
        return jsonify({"error": "Arama sırasında bir hata oluştu", "detail": str(e)}), 502

    if not results:
        return jsonify({"message": "Sonuç bulunamadı"}), 404

    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
