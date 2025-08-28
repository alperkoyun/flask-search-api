from flask import Flask, request, jsonify
from flask_cors import CORS
from googlesearch import search
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# UA'lar
USER_AGENT_MOBILE = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148"
)
USER_AGENT_DESKTOP = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Güvenli bir requests Session (retry + kısa timeoutlar)
def make_session():
    sess = requests.Session()
    retry = Retry(
        total=2,                # en fazla 2 tekrar
        backoff_factor=0.3,     # 0.3s, 0.6s
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)
    return sess

SESSION = make_session()

def get_page_details(url: str, user_agent: str):
    """
    Sayfa başlık ve meta description'ı döndürür.
    Zorunlu olarak HIZLI davranır: kısa connect/read timeout ve tüm hataları yutar.
    """
    headers = {"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"}
    # connect timeout 2s, read timeout 3s -> toplam en çok ~5s/istek
    TIMEOUT = (2, 3)
    try:
        resp = SESSION.get(url, timeout=TIMEOUT, headers=headers, allow_redirects=True)
        # İçerik çok büyükse gereksiz bellek harcamayalım
        if int(resp.headers.get("Content-Length", "0") or 0) > 2_000_000:
            return "Başlık alınamadı", "Açıklama alınamadı"
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "Başlık bulunamadı"
        desc = soup.find("meta", attrs={"name": "description"})
        description = (
            desc.get("content", "").strip() if desc and desc.get("content") else "Açıklama bulunamadı"
        )
        return title, description
    except requests.exceptions.Timeout:
        return "Zaman aşımı", "Açıklama alınamadı"
    except Exception:
        return "Başlık alınamadı", "Açıklama alınamadı"

def google_search_to_json(query, dil="tr", bolge="tr", device=None, site_filter=None, meta=True):
    """
    Google araması yapar, ilk 10 sonucu döndürür.
    meta=True ise sayfaya gidip başlık/description çekmeye çalışır; False ise sadece URL/domain döner.
    """
    results = []
    user_agent = USER_AGENT_MOBILE if device == "mobile" else USER_AGENT_DESKTOP

    # googlesearch-python parametreleri
    search_params = {
        "num_results": 20,
        "lang": dil or "tr",
        
    }

    for i, url in enumerate(search(query, **search_params), start=1):
        domain = urlparse(url).netloc
        if meta:
            title, description = get_page_details(url, user_agent)
        else:
            title, description = "Başlık alınmadı (meta=0)", "Açıklama alınmadı (meta=0)"

        result = {
            "sira": i,
            "url": url,
            "domain": domain,
            "baslik": title,
            "aciklama": description,
            "hedef_site_mi": (site_filter in url) if site_filter else False,
        }
        results.append(result)

    return results

@app.route("/search", methods=["GET"])
def search_api():
    query = request.args.get("query")
    dil = request.args.get("dil")
    bolge = request.args.get("bolge")
    device = request.args.get("device", "desktop")
    site_filter = request.args.get("site_filter")
    # meta: "1" (varsayılan) → başlık/desc çekmeye çalış; "0" → hızlı mod (URL/domain)
    meta_flag = request.args.get("meta", "1")  # "1" / "0"
    meta = meta_flag != "0"

    # Tüm parametreler sizde zorunlu; eksikse 400 dönelim.
    if not all([query, dil, bolge, device, site_filter]):
        return jsonify({"error": "query, dil, bolge, device, site_filter zorunludur"}), 400

    results = google_search_to_json(
        query=query, dil=dil, bolge=bolge, device=device, site_filter=site_filter, meta=meta
    )

    if not results:
        return jsonify({"message": "Sonuç bulunamadı"}), 404
    return jsonify(results)

if __name__ == "__main__":
    # Render için 0.0.0.0/5000
    app.run(host="0.0.0.0", port=5000)
