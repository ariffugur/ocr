import requests

import config


class OcrError(Exception):
    """OCR.space cagrisi basarisiz oldugunda veya beklenmedik yanit
    dondugunde firlatilir. routes.py bunu yakalayip kullaniciya
    anlasilir bir hata mesaji dondurur."""


def recognize_text(base64_image):
    """
    base64_image: 'data:image/jpeg;base64,....' formatinda bir string
    (tarayicidan canvas.toDataURL() ile geliyor).

    OCR.space'e gonderir, taninan duz metni (ParsedText) dondurur.
    Metin bulunamazsa bos string dondurur.
    """
    payload = {
        "apikey": config.OCR_SPACE_API_KEY,
        "base64Image": base64_image,
        "language": config.OCR_SPACE_LANGUAGE,
        "OCREngine": config.OCR_SPACE_ENGINE,
        # scale=true: kucuk/dusuk cozunurluklu goruntuleri OCR.space
        # kendi tarafinda buyuterek okuma basarisini artirir.
        "scale": "true",
        "isOverlayRequired": "false",
        # Ambalaj fotolarinda genelde tek blok/dagimik metin var,
        # otomatik yon algilama faydali.
        "detectOrientation": "true",
    }

    try:
        resp = requests.post(config.OCR_SPACE_URL, data=payload, timeout=25)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OcrError(f"OCR.space'e baglanilamadi: {exc}") from exc

    try:
        data = resp.json()
    except ValueError as exc:
        raise OcrError("OCR.space'ten gecersiz yanit alindi") from exc

    if data.get("IsErroredOnProcessing"):
        message = data.get("ErrorMessage") or data.get("ErrorDetails") or "bilinmeyen hata"
        if isinstance(message, list):
            message = "; ".join(message)
        raise OcrError(f"OCR.space hatasi: {message}")

    results = data.get("ParsedResults") or []
    if not results:
        return ""

    return results[0].get("ParsedText") or ""
