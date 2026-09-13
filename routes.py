from flask import Blueprint, jsonify, render_template, request

import database
from ocr import OcrError, recognize_text

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/api/products", methods=["GET"])
def products():
    """
    Frontend'in OCR ciktisini karsilastirmasi icin gecerli tum
    urun anahtar kelimelerini (whitelist) dondurur.
    """
    urunler = sorted(database.get_all_urunler())
    return jsonify({"urunler": urunler})


@api.route("/api/ocr", methods=["POST"])
def ocr():
    """
    Body: {"image": "data:image/jpeg;base64,...."}
    Tarayicidan gelen kamera karesini OCR.space'e gonderir, taninan
    metni dondurur. Whitelist ile eslestirme islemi frontend'de
    (findMatch) devam ediyor - burasi sadece metni okuyor.
    """
    data = request.get_json(silent=True) or {}
    image = data.get("image") or ""

    if not image:
        return jsonify({"error": "image bos olamaz"}), 400

    try:
        text = recognize_text(image)
    except OcrError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify({"text": text})


@api.route("/api/check-product", methods=["POST"])
def check_product():
    """
    Body: {"sorgu": "bounty"}
    OCR'dan bulunan/whitelist ile eslesen anahtar kelimeyi alir,
    veritabanindan urun bilgisini dondurur.
    """
    data = request.get_json(silent=True) or {}
    sorgu = (data.get("sorgu") or "").strip()

    if not sorgu:
        return jsonify({"found": False, "error": "sorgu bos olamaz"}), 400

    product = database.get_product(sorgu)

    if product is None:
        return jsonify({"found": False}), 404

    return jsonify({"found": True, "product": product})
