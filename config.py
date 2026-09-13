import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")

# OCR.space API ayarlari.
# API key'i asla koda gomme: Render'da "Environment" sekmesinden
# OCR_SPACE_API_KEY adiyla bir env var olarak ekle.
# Key yoksa OCR.space'in herkese acik "helloworld" test key'ine duser -
# bu key cok kisitli (dusuk hiz limiti, kucuk boyut limiti), sadece
# yerel denemeler icindir, sunum gununde kendi ucretsiz key'ini kullan.
# Ucretsiz key: https://ocr.space/ocrapi adresinden e-posta ile aliniyor.
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", "helloworld")
OCR_SPACE_URL = "https://api.ocr.space/parse/image"
OCR_SPACE_ENGINE = os.environ.get("OCR_SPACE_ENGINE", "2")  # Engine 2: daha yeni, cogu durumda daha isabetli
OCR_SPACE_LANGUAGE = os.environ.get("OCR_SPACE_LANGUAGE", "eng")
